import requests
import re
from datetime import datetime

# Conection data
PROJECT_DB_MANAGER_KEY = "."
PROJECT_DB_ID = "."

# CLIENT DATA BASE

HEADERS = {
    "Authorization": f"Bearer {PROJECT_DB_MANAGER_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def main(p_name, ubicacion, tipo):
    data = make_request(PROJECT_DB_ID, HEADERS)
    pages = process_data(data)
    last_project_id = get_project_id(pages)
    project_id = new_project_id(last_project_id)

    valid_name = check_project_name(pages, p_name)

    data = page_data(project_id, valid_name, ubicacion, tipo)

    result = create_page(data, PROJECT_DB_ID, HEADERS)
    print(result)


def make_request(data_id: str, headers: dict):
    """It's access the notion database to get the pages needed,
    the access key goes in the headers and the page for
    the database goes in the data_id"""

    url = f"https://api.notion.com/v1/databases/{data_id}/query"
    response = requests.post(url, headers=headers)

    try:
        response.raise_for_status()

        # Catch all kind of HTTPErrors to inform the final user
    except requests.exceptions.HTTPError as error:
        raise ValueError(f"Error encounter: {error}")
    except requests.exceptions.ConnectionError:
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

    # To avoid incresing the time complexity we just check the first item
    first_page = next(iter(pages))

    properties = first_page["properties"]
    keys = list(properties.keys())

    return keys


def check_properties(properties: list):
    """Contains a list of all the headers needed,
    and the value they should have"""

    correct_properties = [
        "Project",
        "ID",
        "Client",
        "Location",
        "Project Type",
    ]

    for propertie in correct_properties:
        if propertie not in properties:
            raise ValueError(
                "headers do not math database, correct headers are: Project, ID, Client, Location, Project Type"
            )

    return correct_properties


def get_project_id(pages: dict):
    """Get the Project IDs for each proyect puts them on a list,
    sorts them and return the last Project ID"""

    projects_id = []
    for page in pages:
        project_id = page["properties"]["ID"]["rich_text"]
        if len(project_id) > 0:
            id_value = project_id[0]["text"]["content"]
            projects_id.append(id_value)
    sort_ids = sorted(projects_id)
    return sort_ids[-1]


def new_project_id(project_id: str):
    """The Project ID its set by the current year, plus a letter and 2 digits.
    This allow multiple Project IDs and each year it resets.

    It will return ValueError if the Project ID its not correct or the Project ID limit
    its reach"""

    year = datetime.today().year

    # It catchs only the letter and ending number of the Project ID to set new Project ID.
    match = re.match(r"\d+([A-Z])(\d+)", project_id)
    if not match:
        raise ValueError("Project ID format its not correct")

    letter, ending = match.groups()
    new_ending = int(ending) + 1
    if new_ending > 99:
        new_ending = 0
        letter = chr(ord(letter) + 1)
        if letter > "Z":
            raise ValueError("Project ID limit reach, review the Project ID sistem")

    return f"{str(year)[-2:]}{letter}{new_ending:02}"


def check_project_name(pages: dict, name: str):
    """Return a list with all the project names"""

    project_names = []
    for page in pages:
        project_name = page["properties"]["Project"]["title"][0]["text"]["content"]
        project_names.append(project_name)

    if name in project_names:
        raise ValueError("Name already exists")
    else:
        return name


def page_data(
    p_name: str,
    project_id: str,
    client: str,
    project_type: str,
    location: str,
):
    """Creates a dict with all the data need to create the page.
    The data needed is:
    "Project"(title), "Codigo"(rich_text), "Client"(rich_text),
    "Location(rich_text)", "Project Type"(multi_select)"""

    data = {
        "Project": {"title": [{"text": {"content": p_name}}]},
        "ID": {"rich_text": [{"text": {"content": project_id}}]},
        "Client": {"rich_text": [{"text": {"content": client}}]},
        "Location": {"rich_text": [{"text": {"content": location}}]},
        "Project Type": {"multi_select": [{"name": project_type}]},
    }
    return data


def create_page(data: dict, page_id: str, headers: dict):
    """Creates a new page on the database selected."""

    create_url = "https://api.notion.com/v1/pages"

    payload = {"parent": {"database_id": page_id}, "properties": data}

    res = requests.post(create_url, headers=headers, json=payload)

    try:
        res.raise_for_status()
        return "Notion page created"
        # Catch all kind of HTTPErrors to inform the final user
    except requests.exceptions.HTTPError as error:
        raise ValueError(f"Error encounter: {error}")
    except requests.exceptions.ConnectionError as error:
        raise ValueError(f"A connection error ocurred")


if __name__ == "__main__":
    pass
