import pytest
from unittest.mock import Mock
from conectors.notion_conector import *

# Notion_conector Test

# FIXTURES


@pytest.fixture
def pages():
    return [
        {
            "properties": {
                "Project": {"title": [{"text": {"content": "Project 1"}}]},
                "ID": {"rich_text": [{"text": {"content": "24A01"}}]},
                "Client": {"rich_text": [{"text": {"content": "Client 1"}}]},
                "Location": {"rich_text": [{"text": {"content": "Santiago, CL"}}]},
                "Project Type": {"multi_select": [{"name": "Sanitario"}]},
            }
        },
        {
            "properties": {
                "Project": {"title": [{"text": {"content": "Project 2"}}]},
                "ID": {"rich_text": [{"text": {"content": "24A02"}}]},
                "Client": {"rich_text": [{"text": {"content": "Client 2"}}]},
                "Location": {"rich_text": [{"text": {"content": "Madrid, ESP"}}]},
                "Project Type": {"multi_select": [{"name": "Hotelero"}]},
            }
        },
        {
            "properties": {
                "Project": {"title": [{"text": {"content": "Project 3"}}]},
                "ID": {"rich_text": [{"text": {"content": "24Z99"}}]},
                "Client": {"rich_text": [{"text": {"content": "Client 3"}}]},
                "Location": {"rich_text": [{"text": {"content": "Barcelona, ESP"}}]},
                "Project Type": {"multi_select": [{"name": "Residencial"}]},
            }
        },
    ]


@pytest.fixture
def wrong_properties():
    return [
        "Project",
        "Codigo",
        "Clients",
        "Ubicacion",
        "Project Type",
    ]

    #  correct_properties = [
    #     "Project",
    #     "ID",
    #     "Client",
    #     "Location",
    #     "Project Type",
    # ]


@pytest.fixture
def empty_data():
    mock_response = Mock()
    mock_response.json.return_value = {}
    return mock_response


# TESTING NOTION


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
        match="headers do not math database, correct headers are: Project, ID, Client, Location, Project Type",
    ):
        check_properties(wrong_properties)


def test_limit_project_id(pages):

    limit_project_id = get_project_id(pages)

    with pytest.raises(
        ValueError, match="Project ID limit reach, review the Project ID sistem"
    ):
        new_project_id(limit_project_id)


def test_check_project_name(pages):

    with pytest.raises(ValueError, match="Name already exists"):
        check_project_name(pages, "Project 1")


def test_creation():
    data = make_request(PROJECT_DB_ID, HEADERS)
    data_pages = process_data(data)
    last_project_id = get_project_id(data_pages)
    project_id = new_project_id(last_project_id)

    valid_name = check_project_name(data_pages, "Test_project")

    data = page_data(
        valid_name, project_id, "Test_Client", "Test_location", "Test_type"
    )

    create_page(data, PROJECT_DB_ID, HEADERS)
