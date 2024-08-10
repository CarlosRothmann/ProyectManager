import pytest
from unittest.mock import Mock
from notion_conector import *
import project as proj
from pathlib import Path

#Notion_conector Test

#TO DO:
#Add Async to the test to speed up the wait between responses


#FIXTURES

@pytest.fixture
def long_name():
    return "Nombre de mas de cinco palabras"


# TESTING PROJECT

def test_directory():
    
    directory = proj.main_directory()
    
    assert directory
    
def test_check_directory_name(long_name):
    
    with pytest.raises(
        ValueError, 
        match="Name must have between 2 and 5 words"
        ):
        
        proj.check_directory_name(long_name)
        
def test_create_directory():
    
    test_directory = proj.main_directory()
    code = "24XXX"
    name = "TEST"
    
    new_directory = proj.create_directory(test_directory, code, name)
    assert Path(
        "C:\\Users\\User\\Documents\\GitHub\\ProyectManager\\test_projects\\24XXX-TEST"
        ).exists()