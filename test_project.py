import pytest
import project as proj
from pathlib import Path
import shutil

#Notion_conector Test

#TO DO:
#Add Async to the test to speed up the wait between responses


#FIXTURES

@pytest.fixture
def long_name():
    return "Nombre de mas de cinco palabras"

@pytest.fixture
def path():
    dir_path = Path(
        "C:\\Users\\User\\Documents\\GitHub\\ProyectManager\\test_projects\\24XXX-TEST"
        )
    return dir_path
    

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
        
def test_empty_name():
    
    empty_name = ""
    
    with pytest.raises(ValueError):
        proj.check_directory_name(empty_name)

def test_invalid_characters():
    
    # INVALID_CHARACTERS = r"""<>:"/\|?*"""
    
    invalid_name = "Project<"
    with pytest.raises (
        ValueError):
        proj.check_directory_name(invalid_name)

def test_name_long(): 
    
    long_name = "AQSWEDRFTGYHUJIKOLPÑAZSXDCFVGBHNJMKLORETO"
    
    with pytest.raises(ValueError):
        proj.check_directory_name(long_name)
        
def test_name_short(): 
    
    short_name = "AQSW"
    
    with pytest.raises(ValueError):
        proj.check_directory_name(short_name)
        
def test_create_directory(path):
    
    dir_path = path
    
    if dir_path.exists():
        shutil.rmtree(dir_path)
    
    test_directory = proj.main_directory()
    project_id  = "24XXX"
    name = "TEST"
    
    proj.create_directory(test_directory, project_id, name)
    assert dir_path.exists()
    
def test_create_subdirectories(path):
    
    proj.make_subdirectories(path)
    
    assert path.exists()
    
def test_copy_files():
    
    project_id = "24XXX"
    source = Path(
        "C:\\Users\\User\\Documents\\GitHub\\ProyectManager\\base_files\\XXXX-BIM-ZZ-DOC-PlantillaBEP.docx"
        )
    destination_path = Path("C:\\Users\\User\\Documents\\GitHub\\ProyectManager\\test_projects\\24XXX-TEST\\30-BIM\\31-GESTION")
    
    proj.copy_files(source, destination_path, project_id)
    
    assert Path(
        "C:\\Users\\User\\Documents\\GitHub\\ProyectManager\\test_projects\\24XXX-TEST\\30-BIM\\31-GESTION\\24XXX-BIM-ZZ-DOC-PlantillaBEP.docx"
        ).exists()