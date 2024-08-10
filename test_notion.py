import pytest
from unittest.mock import Mock
from notion_conector import *

#Notion_conector Test

#TO DO:
#Add Async to the test to speed up the wait between responses


#FIXTURES

@pytest.fixture
def pages():
    return [
        {
            "properties": {
                "Proyecto": {"title": [{"text": {"content": "Proyecto 1"}}]},
                "Código": {"rich_text": [{"text": {"content": "24A01"}}]},
                "Cliente": {"rich_text": [{"text": {"content": "Client 1"}}]},
                "Ubicación": {"rich_text": [{"text": {"content": "Santiago, CL"}}]},
                "Tipo proyecto": {"multi_select": [{"name": "Sanitario"}]}
            }
        },
        {
            "properties": {
                "Proyecto": {"title": [{"text": {"content": "Proyecto 2"}}]},
                "Código": {"rich_text": [{"text": {"content": "24A02"}}]},
                "Cliente": {"rich_text": [{"text": {"content": "Client 2"}}]},
                "Ubicación": {"rich_text": [{"text": {"content": "Madrid, ESP"}}]},
                "Tipo proyecto": {"multi_select": [{"name": "Hotelero"}]}
            }
        },
        {
            "properties": {
                "Proyecto": {"title": [{"text": {"content": "Proyecto 3"}}]},
                "Código": {"rich_text": [{"text": {"content": "24Z99"}}]},
                "Cliente": {"rich_text": [{"text": {"content": "Client 3"}}]},
                "Ubicación": {"rich_text": [{"text": {"content": "Barcelona, ESP"}}]},
                "Tipo proyecto": {"multi_select": [{"name": "Residencial"}]}
            }
        }
    ]

@pytest.fixture
def wrong_properties():
    return [
        "Proyecto",
        "Codigo",
        "Clientes", 
        "Ubicacion",
        "Tipo proyecto",
    ]

    #  correct_properties = [
    #     "Proyecto",
    #     "Código",
    #     "Cliente",
    #     "Ubicación",
    #     "Tipo proyecto",
    # ]

@pytest.fixture
def empty_data():
    mock_response = Mock()
    mock_response.json.return_value = {}
    return mock_response

@pytest.fixture
def long_name():
    return "Nombre de mas de cinco palabras"

#TESTING NOTION


def test_connecion():
    
    response = make_request(PROJECT_DB_ID, HEADERS)

    assert response.status_code == 200 
    
def test_empty_data(empty_data):
    
    with pytest.raises(ValueError, match="Response data is empty"):
        process_data(empty_data)

def test_process_data():
    
    data = make_request(PROJECT_DB_ID, HEADERS)
    pages = process_data(data)    
    
    assert pages

def test_check_properties(wrong_properties):
    
    with pytest.raises(
        ValueError, 
        match= "headers do not math database, correct headers are: Proyecto, Código, Cliente, Ubicación, Tipo proyecto"
        ):
        check_properties(wrong_properties)

def test_limit_code(pages):
    
    limit_code = get_project_id(pages)
    
    with pytest.raises(
        ValueError, 
        match="Code limit reach, review the code sistem"
        ):
        new_code(limit_code)

def test_check_project_name(pages):
    
    with pytest.raises(ValueError, match="Name already exists"):
        check_project_name(pages, "Proyecto 1")
        
def test_creation():
    data = make_request(PROJECT_DB_ID, HEADERS)
    data_pages = process_data(data)
    last_code = get_project_id(data_pages)
    code = new_code(last_code)
    
    valid_name = check_project_name(data_pages, "Test_project2")
    
    data = page_data(valid_name, code,"Test_cliente", "Test_ubicacion", "Test_tipo")

    create_page(data, PROJECT_DB_ID, HEADERS) 
