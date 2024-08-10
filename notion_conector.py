import requests
import re
from datetime import datetime

#Conection data
PROJECT_DB_MANAGER_KEY = "secret_yHa3RYk1PlIzgpbOYDSBv1y5lZ0jdyxaHtYgNOgF9dI"
PROJECT_DB_ID = "14ccd3058a2f4b6eabc2a18686e00972"


#CLIENT DATA BASE

HEADERS = {
    "Authorization" : f"Bearer {PROJECT_DB_MANAGER_KEY}",
    "Content-Type" : "application/json",
    "Notion-Version" : "2022-06-28",
}

def main(p_name, ubicacion, tipo):
    data = make_request(PROJECT_DB_ID, HEADERS)
    pages = process_data(data)
    last_code = get_project_id(pages)
    code = new_code(last_code)
    
    valid_name = check_project_name(pages, p_name)
    
    data = page_data(code, valid_name, ubicacion, tipo)

    result = create_page(data, PROJECT_DB_ID, HEADERS)
    print(result) 
      
    
    
def make_request(data_id: str, headers:dict):
    
    """It's access the notion database to get the pages needed,
    the access key goes in the headers and the page for
    the database goes in the data_id"""
    
    url =f"https://api.notion.com/v1/databases/{data_id}/query"
    response = requests.post(url, headers=headers)
    
    try: 
        response.raise_for_status()
        
        #Catch all kind of HTTPErrors to inform the final user
    except requests.exceptions.HTTPError as error:
        raise ValueError(f"Error encounter: {error}")
    except requests.exceptions.ConnectionError as error:
        raise ValueError(f"A connection error ocurred")
        
    return response

def process_data(response):
    
    try:
        data = response.json()
    except ValueError:
        raise ValueError("Invalid JSON response")
    
    if not data:
        raise ValueError("Response data is empty")
    
    return data["results"]

def get_properties(pages: dict):
    
    """It's return a list with the headers of the database"""
    
    #To avoid incresing the time complexity we just check the first item
    first_page = next(iter(pages))
    
    properties = first_page["properties"]
    keys = list(properties.keys())

    return keys
        
def check_properties(properties: list):
    
    """Contains a list of all the headers needed, 
    and the value they should have"""
    
    correct_properties = [
        "Proyecto",
        "Código",
        "Cliente",
        "Ubicación",
        "Tipo proyecto",
    ]
    
    for propertie in correct_properties:
        if propertie not in properties:
            raise ValueError(
                "headers do not math database, correct headers are: Proyecto, Código, Cliente, Ubicación, Tipo proyecto"
                )

    return correct_properties
        
def get_project_id(pages: dict):
    
    """Get the codes for each proyect puts them on a list, 
    sorts them and return the last code"""
    
    projects_id = []
    for page in pages:
        project_id = page["properties"]["Código"]["rich_text"]
        if len(project_id) > 0:
            id_value = project_id[0]["text"]["content"]
            projects_id.append(id_value)
    sort_ids = sorted(projects_id)
    return sort_ids[-1]
    
def new_code(project_id: str):
    
    """The code its set by the current year, plus a letter and 2 digits.
    This allow multiple codes and each year it resets.
    
    It will return ValueError if the code its not correct or the code limit
    its reach"""
    
    year = datetime.today().year
    
    #It catchs only the letter and ending number of the code to set new code.
    match = re.match(r"\d+([A-Z])(\d+)", project_id)
    if not match:
        raise ValueError("Code format its not correct")
    
    letter, ending = match.groups()
    new_ending = int(ending) + 1
    if new_ending > 99:
        new_ending = 0
        letter = chr(ord(letter)+1)
        if letter > "Z":
            raise ValueError("Code limit reach, review the code sistem")
    
    return f"{str(year)[-2:]}{letter}{new_ending:02}"

def check_project_name(pages: dict, name: str):
    
    """Return a list with all the project names"""
    
    project_names = []
    for page in pages:
        project_name = page["properties"]["Proyecto"]["title"][0]["text"]["content"]
        project_names.append(project_name)
        
    if name in project_names:
        raise ValueError("Name already exists")
    else:
        return name

def page_data(
    p_name: str, 
    project_id: str, 
    cliente: str, 
    ubicacion: str, 
    tipo: str,
    ):
    
    """Creates a dict with all the data need to create the page. 
    The data needed is:
    "Proyecto"(title), "Codigo"(rich_text), "Cliente"(rich_text), 
    "Ubicación(rich_text)", "Tipo proyecto"(multi_select)"""
    
    data = {
        "Proyecto" : {"title" : [{"text":{"content": p_name}}]},
        "Código" : {"rich_text" : [{"text":{"content": project_id}}]},
        "Cliente" : {"rich_text" : [{"text":{"content": cliente}}]},
        "Ubicación" : {"rich_text" : [{"text":{"content": ubicacion}}]}, 
        "Tipo proyecto" : {"multi_select": [{"name": tipo}]}
    }
    return data

def create_page(data: dict, page_id: str, headers:dict):
    
    
    """Creates a new page on the database selected."""
    
    create_url = "https://api.notion.com/v1/pages"
    
    payload = {"parent": {"database_id": page_id}, "properties":data}
    
    res = requests.post(create_url, headers=headers, json=payload)

    try: 
        res.raise_for_status()
        return "Page created"
        #Catch all kind of HTTPErrors to inform the final user
    except requests.exceptions.HTTPError as error:
        raise ValueError(f"Error encounter: {error}")
    except requests.exceptions.ConnectionError as error:
        raise ValueError(f"A connection error ocurred")

    
if __name__ == "__main__":
    main("Proyecto prueba con Main", "Hogar, ESP", "Sostenibilidad")