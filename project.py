from pathlib import Path
import gui
import shutil
import json
from conectors.notion_conector import *
import tkinter as tk
from tkinter import messagebox, filedialog


# CONSTANTS

INVALID_CHARACTERS = r"""<>:"/\|?*"""

PROJECT_TYPES = [
    "Residential",
    "Educational",
    "Healthcare",
    "Office",
    "Landscaping",
    "Transport",
    "Master Plan",
    "Recreational",
    "Interior Design",
    "Hotel",
    "Sport"
]

SETTINGS = "user_settings.json"

# MAIN


def main():

    creation_result = []
    # Try collecting data from Notion if and error happend a message will display
    try:
        notion_data = make_request(PROJECT_DB_ID, HEADERS)

        pages = process_data(notion_data)
        last_project_id = get_project_id(pages)
        project_id = new_project_id(last_project_id)
    except Exception as notion_error:
        messagebox.showerror("Error", f"An error ocurred: {notion_error}")

    # Collect the entry's of the UI
    values = [
        name_string.get(),
        client_string.get(),
        option_string.get(),
        location_string.get(),
    ]

    # CHECKING PROJECTS NAMES

    try:
        checked_directory = check_directory_name(values[0])
        valid_name = check_project_name(pages, checked_directory)
    except Exception as name_error:
        messagebox.showerror("Error", f"An error ocurred: {name_error}")

    # CHECKING NOTION COLUMN HEADRES

    properties = get_properties(pages)
    try:
        check_properties(properties)
    except Exception as name_error:
        messagebox.showerror("Error", f"An error ocurred: {name_error}")

    # CREATE DIRECTORIES AND COPY FILES

    root = main_directory(SETTINGS)

    new_directory = create_directory(root, project_id, valid_name)
    creation_result.append(new_directory[1])

    directory_result = make_subdirectories(new_directory[0], SETTINGS)
    creation_result.append(directory_result)

    source = source_directory(SETTINGS)
    if source != "No directory selected... ":

        file_destination = Path(new_directory[0] / "30-BIM\\31-GESTION")
        files = copy_files(source, file_destination, project_id)
        creation_result.append(files)

    # CREATE NOTION PAGE

    project_info = page_data(valid_name, project_id, values[1], values[2], values[3])

    try:
        new_page = create_page(project_info, PROJECT_DB_ID, HEADERS)
        creation_result.append(new_page)
    except Exception as name_error:
        messagebox.showerror("", f"{name_error}")

    formatted_result = "\n".join(creation_result)
    messagebox.showinfo("Results", formatted_result)


# FUNCTIONS


def check_directory_name(name: str):

    pattern = re.compile(f"[{re.escape(INVALID_CHARACTERS)}]")

    if name:
        if bool(pattern.search(name)):
            raise ValueError(f"Name have invalid characters ({INVALID_CHARACTERS})")
        elif len(name) < 5 or len(name) > 40:
            raise ValueError("Name have more than 4 letters")
        else:
            words = name.split(" ")
            if len(words) < 2 or len(words) > 5:
                raise ValueError("Name must have between 2 and 5 words")
    else:
        raise ValueError("Project name missing")

    return name.title()


# USER_SETTINGS FILE


def load_settings(file_name: str):
    with open(file_name, "r") as file:
        return json.load(file)


def save_settings(file_name: str, settings):
    with open(file_name, "w") as file:
        json.dump(settings, file, indent=4)


def set_main_directory(file_name: str, title: str):

    # Select the main_directory and save the path to the user_settings.json
    main_directory = filedialog.askdirectory(title=title)

    if main_directory:  # If the user selected a directory
        settings = load_settings(file_name)
        settings["main_directory"] = main_directory
        save_settings(file_name, settings)
    else:  # If the user canceled or closed the dialog
        settings = load_settings(file_name)
        main_directory = settings.get("main_directory", None)

    return main_directory


def set_source_files(file_name: str, title: str):

    # Select the source_directory and save the path to the user_settings.json
    file_directory = filedialog.askdirectory(title=title)

    if file_directory:
        settings = load_settings(file_name)
        settings["file_directory"] = file_directory
        save_settings(file_name, settings)
    else:
        settings = load_settings(file_name)
        file_directory = settings.get("file_directory", None)

    return file_directory


def reset_settings(file_name: str, message: str):

    # Reset the values of the keys on the user_settings.json to null
    settings = load_settings(file_name)
    settings["main_directory"] = None
    settings["file_directory"] = None
    save_settings(file_name, settings)
    return message


# DIRECTORIES AND FILES


def main_directory(path: str):

    settings_path = Path(path)

    # By default the directory where the Python file is located will be the main_directory
    default_directory = Path(__file__).parent

    # Check if the settings file exists
    if settings_path.exists():
        with open(settings_path, "r") as file:
            settings = json.load(file)

        # If main_directory is null or doesn't exist, use the default directory
        main_directory = settings.get("main_directory") or default_directory
    else:
        # If the file doesn't exist, use the default directory
        main_directory = default_directory

    return Path(main_directory)


def source_directory(path: str):

    settings_path = Path(path)

    # Check if the settings file exists
    if settings_path.exists():
        with open(settings_path, "r") as file:
            settings = json.load(file)

        source_directory = settings.get("file_directory")
        if source_directory == None:
            return "No directory selected... "
        else:
            return Path(source_directory)
    else:
        # If the file doesnt exists use None because its the value in case
        # the source its not define
        return "No directory selected... "


def create_directory(path, project_id, name):

    new_directory = Path(path / f"{project_id}-{name}")
    new_directory.mkdir(parents=True, exist_ok=True)
    return new_directory, f"Directory created at {new_directory}"


def make_subdirectories(path: str, json_file: str):
    # Load the folder structure from the JSON file
    with open(json_file, 'r') as file:
        data = json.load(file)
        folder_structure = data.get("folder_structure")

    for main_folder, subfolders in folder_structure.items():
        main_folder_path = Path(path) / main_folder
        main_folder_path.mkdir(parents=True, exist_ok=True)

        # Iterate over each subfolder in the main folder
        for subfolder in subfolders:
            subfolder_path = main_folder_path / subfolder
            subfolder_path.mkdir(parents=True, exist_ok=True)

    return "Subdirectories created"


def copy_files(source, directory, project_id):

    # Convert to Paths
    destination = Path(directory)

    # Check if the source directory exists
    if source.exists() and source.is_dir():
        count = 0
        for file in source.iterdir():
            if file.is_file():
                # Create the new file name with the project ID
                file_name = file.name
                new_name = f"{project_id}{file_name[5:]}"
                final_destination = destination / new_name
                shutil.copy(file, final_destination)
                count += 1
        return f"{count} files copied successfully."
    else:
        return f"Source directory {source} not found or is not a directory."


if __name__ == "__main__":

    # GUI
    size = (400, 600)

    app = gui.Application(size, "BIM Project Starter")
    tabs = gui.Tab(app, size)

    # CREATION TABS
    # Entrys
    name_string = tk.StringVar()
    gui.Entry_Segment(
        tabs.tab("Create"),
        "PROJECT NAME",
        name_string,
        "Use between 2 to 5 words "
    )

    client_string = tk.StringVar()
    gui.Entry_Segment(
        tabs.tab("Create"),
        "CLIENT",
        client_string,
        ""
        )

    option_string = tk.StringVar()
    gui.Dropdown_Segment(
        tabs.tab("Create"),
        "PROJECT TYPE",
        PROJECT_TYPES,
        option_string,
        "Choose the main one, others can be added on notion ",
    )

    location_string = tk.StringVar()
    gui.Entry_Segment(
        tabs.tab("Create"),
        "LOCATION",
        location_string,
        "City, COUNTRY "
        )

    # Execution
    gui.Confirmation_Button(tabs.tab("Create"), "Create Project ", lambda: main())

    # SETTINGS TABS
    main_string = tk.StringVar(value=main_directory(SETTINGS))
    source_string = tk.StringVar(value=source_directory(SETTINGS))

    def reset():
        reset_settings(SETTINGS, "Settings values erased")
        main_string.set(value=main_directory(SETTINGS))
        source_string.set(value=source_directory(SETTINGS))

    gui.Setting_button(
        tabs.tab("Settings"),
        "Main directory:",
        main_string,
        "Select directory...",
        lambda: main_string.set(set_main_directory(SETTINGS, "Select main directory")),
    )

    gui.Setting_button(
        tabs.tab("Settings"),
        "Files source: ",
        source_string,
        "Select directory...",
        lambda: source_string.set(set_source_files(SETTINGS, "Select files directory")),
    )

    gui.Confirmation_Button(tabs.tab("Settings"), "Reset Settings", lambda: reset())

    #DIR STRUCTURE TAB

    gui.Folder_Struc(tabs.tab("Dir Structure"), SETTINGS)

    app.mainloop()
