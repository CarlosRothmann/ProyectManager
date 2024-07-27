import requests
import json
from datetime import datetime, timezone

#Conection data
PROJECT_DB_MANAGER_KEY = "secret_yHa3RYk1PlIzgpbOYDSBv1y5lZ0jdyxaHtYgNOgF9dI"
PROJECT_DB_ID = "14ccd3058a2f4b6eabc2a18686e00972"


headers = {
    "Authorization" : f"Bearer {PROJECT_DB_MANAGER_KEY}",
    "Content-Type" : "application/json",
    "Notion-Version" : "2022-06-28",
}

def get_pages():
    url =f"https://api.notion.com/v1/databases/{PROJECT_DB_ID}/query"

    response = requests.post(url, headers=headers)
    
    data = response.json()
    return data["results"]


if __name__ == "__main__":
    pages = get_pages()
    
    """The key for the properties are the name of the columns on the notion database
    Each of these properties has a type, are information its store on key with the 
    same name as the type. List of type and the key values for its content:
    - "checkbox"
    - "created_by"
    - "created_time"
    - "date"
    - "email"
    - "files"
    - "formula"
    - "last_edited_by"
    - "last_edited_time"
    - "multi_select"
    - "number"
    - "people"
    - "phone_number"
    - "relation"
    - "rich_text: text: content"
    - "rollup"
    - "select: name"
    - "status: name"
    - "title: text: content"
    - "url"
    """
    
    for page in pages:
        page_id = page["id"]
        properties = page["properties"]
        proyecto = properties["Proyecto"]["title"][0]["text"]["content"]
        codigo = properties["Codigo"]
        cliente = properties["Cliente"]
        fase_desarollo = properties["Fase desarrollo"]
        status = properties["Estado"]
        responsable = properties["Responsable Proyecto"]
        # print(page_id, json.dumps(properties, indent=1))
        print(properties.keys())
        print(proyecto)
        