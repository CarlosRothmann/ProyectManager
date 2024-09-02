import pytest
import project as proj
from pathlib import Path
import shutil


# FIXTURES


@pytest.fixture
def long_name():
    return "Nombre de mas de cinco palabras"


@pytest.fixture
def root_path():
    return Path(__file__).parent

@pytest.fixture
def settings():
    return "user_settings.json"

# TESTING PROJECT


def test_directory():

    directory = proj.main_directory("user_settings.json")

    assert directory


def test_check_directory_name(long_name):

    with pytest.raises(ValueError, match="Name must have between 2 and 5 words"):

        proj.check_directory_name(long_name)


def test_empty_name():

    empty_name = ""

    with pytest.raises(ValueError):
        proj.check_directory_name(empty_name)


def test_invalid_characters():

    # INVALID_CHARACTERS = r"""<>:"/\|?*"""

    invalid_name = "Project<"
    with pytest.raises(ValueError):
        proj.check_directory_name(invalid_name)


def test_name_long():

    long_name = "AQSWEDRFTGYHUJIKOLPÑAZSXDCFVGBHNJMKLORETO"

    with pytest.raises(ValueError):
        proj.check_directory_name(long_name)


def test_name_short():

    short_name = "AQSW"

    with pytest.raises(ValueError):
        proj.check_directory_name(short_name)


def test_create_directory(root_path):

    dir_path = Path(root_path / "24XXX-TEST")

    if dir_path.exists():
        shutil.rmtree(dir_path)

    test_directory = proj.main_directory("user_settings.json")
    project_id = "24XXX"
    name = "TEST"

    proj.create_directory(test_directory, project_id, name)
    assert dir_path.exists()


def test_create_subdirectories(root_path, settings):

    directory_path = Path(root_path / "24XXX-TEST")
    proj.make_subdirectories(directory_path, settings)

    assert directory_path.exists()


def test_copy_files(root_path):

    project_id = "24XXX"

    source = Path(root_path / "base_files")
    destination_path = Path(root_path / r"24XXX-TEST/30-BIM/31-GESTION")

    proj.copy_files(source, destination_path, project_id)

    file_location = Path(
        root_path / r"24XXX-TEST/30-BIM/31-GESTION/24XXX-BIM-ZZ-DOC-PlantillaBEP.docx"
    )
    assert file_location.exists()
