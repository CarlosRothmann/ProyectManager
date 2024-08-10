from pathlib import Path
import gui
import shutil
from notion_conector import *
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

#Definir funcion para crear carpetas
# TO DO 

#CONSTANTS

PROJECT_TIPES = []

#MAIN

def main():
    #GUI
    #Imputs
    inputs = "nombre prueba"
    
    name = check_directory_name(inputs)
    path = main_directory()
    
    
#FUNCTIONS 

def check_directory_name(name: str):

    words = name.split(" ")
    if len(words) < 2 or len(words) > 5:
        raise ValueError("Name must have between 2 and 5 words")
        
    return name

def main_directory():
    directory = Path("C:\\Users\\User\\Documents\\GitHub\\ProyectManager\\test_projects")
    
    if directory.exists():
        return directory
    else:
        raise NameError(
            "Path not found, the path should be: C:\\Users\\User\\OneDrive\\02-Arquitectura\\02-BIM\\99-PROYECTOS"
            )

def create_directory(path ,code, name ):
    
    directory_name = f"{code}-{name}"

    new_directory = Path(path /directory_name)
    new_directory.mkdir(parents=True, exist_ok=True)
    return new_directory

#REVISAR
def make_subdirectories(path):
        
    #Crear subcarpetas
    subcarpetas = ['10-ENVIOS', '20-GESTION', '30-BIM', '40-AP','50-PB','60-PE','70-DF','80-AS-BUILT','90-FOTOS']
    for subcarpeta in subcarpetas:
        subcarpeta_path = Path(path / subcarpeta)
        subcarpeta_path.mkdir(parents=True, exist_ok=True)
            
    #Crear subcarpetas en la carpeta 10-Envios
    sub_10 = ['11-ENVIADOS','12-RECIBIDOS', '13-ENTREGAS']
    for sub_10 in sub_10:
        sub_10_path = Path(path / '10-ENVIOS' / sub_10)
        sub_10_path.mkdir(parents=True, exist_ok=True)
            
    #crear subcarpetas en la carpeta 20-Gestion
    subcarpetas_20 = ['21-NORMATIVA','22-CLIENTE','23-INDUSTRIALES']
    for subcarpeta_20 in subcarpetas_20:
        subcarpeta_20_path = Path(path / '20-GESTION' / subcarpeta_20)
        subcarpeta_20_path.mkdir(parents=True, exist_ok=True)
        
    #Crear subcarpetas en la carpeta 30-BIM
    subcarpetas_30 = ['31-GESTION','32-MODELOS','33-RECURSOS','34-LINKS','35-EXPORTS','36-IMAGENES',"37-TRABAJO"]
    for subcarpeta_30 in subcarpetas_30:
        subcarpeta_30_path = Path(path / '30-BIM' / subcarpeta_30)
        subcarpeta_30_path.mkdir(parents=True, exist_ok=True)
    
def copy_files(source, path):    

    # Copiar un archivos a la subcarpeta '31-Gestion'
    source_file_path = source
    destination_path = Path(path / '30-BIM'/ '31-Gestion')
    # if os.path.exists(source_file_path):
    #     shutil.copy(source_file_path, destination_path)
    #     nombre_archivo = os.path.basename(source_file_path)
    #     mensaje_archivo = f'Archivo copiado {nombre_archivo}'
    # else: 
    #     mensaje_archivo = f'El archivo {source_file_path} no existe o cambio de ubicación'
        
    # Mostrar mensaje emergente con el resultado
    # mensaje_final = f"{mensaje_carpeta}\n{mensaje_archivo}"
    # messagebox.showinfo("Resultado", mensaje_final)
        
        
if __name__ == '__main__':
    main()