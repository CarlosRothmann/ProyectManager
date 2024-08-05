import pytest
import requests
from notion_conector import *
import project as proj

#Notion_conector Test

def test_connecion():
    url = url =f"https://api.notion.com/v1/databases/{PROJECT_DB_ID}/query"
    response = requests.post(url, headers=HEADERS)

    assert response.status_code == 200 

def test_limit_code():
    pass

def test_wrong_code():
    
    wrong_code = "2A345"
    
    assert new_code(wrong_code) == ValueError("Code format its not correct")

def test_check_project_name():
    pass