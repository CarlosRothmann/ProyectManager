from pathlib import Path
import gui
import shutil
from notion_conector import *
import tkinter as tk
from tkinter import messagebox



#CONSTANTS

INVALID_CHARACTERS = r"""<>:"/\|?*"""

PROJECT_TYPES = [
    "Residential" , "Educational" , "Healthcare" , "Office", 
    "Landscaping" , "Transport" , "Master Plan" ,
    "Recreational" , "Interior Design" , "Hotel" ,
]

#MAIN

def main():
   
    #Try collecting data from Notion if and error happend a message will display
    try:
        notion_data = make_request(PROJECT_DB_ID, HEADERS)

        pages = process_data(notion_data)
        last_project_id = get_project_id(pages)
        project_id = new_project_id(last_project_id)
    except Exception as notion_error:
        messagebox.showerror("Error", f"An error ocurred: {notion_error}")
            
    #Collect the entry's of the UI
    values = [
        name_string.get(),
        client_string.get(),
        option_string.get(),
        location_string.get(),
    ]

    #CHECKING PROJECTS NAMES
    
    try:
        checked_directory = check_directory_name(values[0])
        valid_name = check_project_name(pages, checked_directory)
    except Exception as name_error:
        messagebox.showerror("Error", f"An error ocurred: {name_error}")
    
    #CHECKING NOTION COLUMN HEADRES
    
    properties = get_properties(pages)
    try: 
        check_properties(properties)
    except Exception as name_error:
        messagebox.showerror("Error", f"An error ocurred: {name_error}")
    
    #CREATE DIRECTORIES AND COPY FILES
    
    root = main_directory()
    new_directory = create_directory(root, project_id, valid_name)
    make_subdirectories(new_directory)
    
    file_destination = Path(new_directory / "30-BIM\\31-GESTION")
    file1_source = Path(
        "C:\\Users\\User\\Documents\\GitHub\\ProyectManager\\base_files\\XXXXX-BIM-ZZ-DOC-PlantillaBEP.docx"
        )
    file2_source = Path(
        "C:\\Users\\User\\Documents\\GitHub\\ProyectManager\\base_files\\XXXXX-BIM-ZZ-TAB-Indice.xlsx"
        )
    file3_source = Path(
        "C:\\Users\\User\\Documents\\GitHub\\ProyectManager\\base_files\\XXXXX-BIM-ZZ-TAB-keynotes.xlsx"
        )
    
    
    copy_files(file1_source, file_destination, project_id)
    copy_files(file3_source, file_destination, project_id)
    copy_files(file2_source, file_destination, project_id)
    
    
    #CREATE NOTION PAGE
    
    project_info = page_data(
        valid_name, 
        project_id, 
        values[1], 
        values[2], 
        values[3])
    
    try:
        new_page = create_page(project_info, PROJECT_DB_ID, HEADERS)
        messagebox.showinfo("", new_page)
    except Exception as name_error:
        messagebox.showerror("", f"{name_error}")
    
#FUNCTIONS 

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
        
    return name

def main_directory():
    directory = Path("C:\\Users\\User\\Documents\\GitHub\\ProyectManager\\test_projects")
    
    if directory.exists():
        return directory
    else:
        raise NameError(
            "Path not found, the path should be: C:\\Users\\User\\OneDrive\\02-Arquitectura\\02-BIM\\99-ProjectS"
            )

def create_directory(path ,project_id, name ):

    new_directory = Path(path / f"{project_id}-{name}")
    new_directory.mkdir(parents=True, exist_ok=True)
    return new_directory

def make_subdirectories(path):
        
    #Crear subcarpetas
    subcarpetas = ["10-ENVIOS", 
                   "20-GESTION", 
                   "30-BIM", 
                   "40-AP",
                   "50-PB",
                   "60-PE",
                   "70-DF",
                   "80-AS-BUILT",
                   "90-FOTOS"]
    for subcarpeta in subcarpetas:
        subcarpeta_path = Path(path / subcarpeta)
        subcarpeta_path.mkdir(parents=True, exist_ok=True)
            
    #Crear subcarpetas en la carpeta 10-Envios
    subcarpetas_10 = ["11-ENVIADOS","12-RECIBIDOS", "13-ENTREGAS"]
    sub_path10 = Path(path) / "10-ENVIOS"
    for sub_10 in subcarpetas_10:
        sub_path = Path(sub_path10) / sub_10
        sub_path.mkdir(parents=True, exist_ok=True)
            
    #crear subcarpetas en la carpeta 20-Gestion
    subcarpetas_20 = ["21-NORMATIVA","22-CLIENTE","23-INDUSTRIALES"]
    sub_path20 = Path(path) / "20-GESTION"
    
    for subcarpeta_20 in subcarpetas_20:
        subcarpeta_20_path = Path(sub_path20) / subcarpeta_20
        subcarpeta_20_path.mkdir(parents=True, exist_ok=True)
        
    #Crear subcarpetas en la carpeta 30-BIM
    subcarpetas_30 = [
        "31-GESTION",
        "32-MODELOS",
        "33-RECURSOS",
        "34-LINKS",
        "35-EXPORTS",
        "36-IMAGENES",
        "37-TRABAJO",
        ]
    sub_path30 = Path(path) / "30-BIM"
    
    for subcarpeta_30 in subcarpetas_30:
        subcarpeta_30_path = Path(sub_path30) / subcarpeta_30
        subcarpeta_30_path.mkdir(parents=True, exist_ok=True)
    
def copy_files(source, destination, project_id):    

    #Convert to Paths
    source = Path(source)
    destination = Path(destination)

    if source.exists():
        
        #Change the name for the destinacion path.
        file_name = source.name
        new_name = f"{project_id}{file_name[5:]}"
        
        final_destination = destination / new_name
        
        shutil.copy(source, final_destination)
        
        return f"Archivo copiado"
    else: 
        return f"El archivo {source} no existe o cambió de Location"
        
        
if __name__ == "__main__":
    
    #GUI
    app = gui.Application((300, 460), "Project Creator")
    
    #Entrys
    name_string = tk.StringVar()
    gui.Entry_Segment(
        app,
        "PROJECT NAME",
        name_string, 
        "Use between 2 and 5 words ")
    
    client_string = tk.StringVar()
    gui.Entry_Segment(
        app, 
        "CLIENT", 
        client_string, 
        "")
    
    option_string = tk.StringVar()
    gui.Dropdown_Segment(
        app, 
        "PROJECT TYPE",
        PROJECT_TYPES, 
        option_string, 
        "Choose the main one, others can be add on notion "
        )
    
    location_string = tk.StringVar()
    gui.Entry_Segment(
        app,
        "LOCATION", 
        location_string, 
        "City, COUNTRY ")
    
    #Execution
    gui.Confirmation_Button(app, "Create Projet ", lambda: main())
    
    app.mainloop()