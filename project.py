import os
import tkinter
import shutil
from tkinter import simpledialog, filedialog, messagebox
from notion_conector import *
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor

#Definir funcion para crear carpetas
# TO DO 

#Agregar concur

def main():
    name = set_name()
    directory_name()
    make_directories()
    
    
def set_name():
    root = tkinter.Tk()
    root.withdraw()
    
    #Ingresar nombre de la carpeta
    while True:
        nombre_carpeta = simpledialog.askstring(
            title="CREACIÓN DIRECTORIO PROYECTO", 
            prompt="Ingrese el nombre de la carpeta, Ejemplo: 00000-PROYECTO PRUEBA")
    
        if validar_nombre(nombre_carpeta):
            folder_selected = filedialog.askdirectory()
            path = os.path.join(folder_selected, nombre_carpeta)
            if not os.path.exists(path):
                os.makedirs(path)
                mensaje_carpeta = 'Carpeta creada'
                break #Sale si el nombre es correcto
            else:
                messagebox.showerror("Error", "La carpeta ya existe")
        else:
            messagebox.showerror(
                "Error", 
                "Nombre incorrecto. Recuerda que debe tener 5 números, un guion y luego todo en mayúsculas.")

def directory_name(code: str , name: str):
    if not nombre[:5].isdigit():
        return False
    if nombre[5] != "-":
        return False
    if not nombre[6:].isupper():
        return False
    return True

def make_directories(path):
    #Crear ventana para seleccionar la carpeta
        
    #Crear subcarpetas
    subcarpetas = ['10-ENVIOS', '20-GESTION', '30-BIM', '40-AP','50-PB','60-PE','70-DF','80-AS-BUILT','90-FOTOS']
    for subcarpeta in subcarpetas:
        subcarpeta_path = os.path.join(path, subcarpeta)
        os.makedirs(subcarpeta_path)
            
    #Crear subcarpetas en la carpeta 10-Envios
    subcarpetas_10 = ['11-ENVIADOS','12-RECIBIDOS']
    for subcarpeta_10 in subcarpetas_10:
        subcarpeta_10_path = os.path.join(path, '10-ENVIOS', subcarpeta_10)
        os.makedirs(subcarpeta_10_path)
            
    #crear subcarpetas en la carpeta 20-Gestion
    subcarpetas_20 = ['21-NORMATIVA','22-CLIENTE','23-INDUSTRIALES']
    for subcarpeta_20 in subcarpetas_20:
        subcarpeta_20_path = os.path.join(path, '20-GESTION', subcarpeta_20)
        os.makedirs(subcarpeta_20_path)
        
    #Crear subcarpetas en la carpeta 30-BIM
    subcarpetas_30 = ['31-GESTION','32-MODELOS','33-RECURSOS','34-LINKS','35-EXPORTS','36-IMAGENES',"37-TRABAJO"]
    for subcarpeta_30 in subcarpetas_30:
        subcarpeta_30_path = os.path.join(path, '30-BIM', subcarpeta_30)
        os.makedirs(subcarpeta_30_path)
    
    # Copiar un archivos a la subcarpeta '31-Gestion'
    source_file_path = "C:\\Users\\User\\OneDrive\\02-Arquitectura\\02-BIM\\01-Revit\\00-Config\\RA-RVT-ParametrosCompartidos.txt"
    destination_path = os.path.join(path, '30-BIM', '31-Gestion')
    if os.path.exists(source_file_path):
        shutil.copy(source_file_path, destination_path)
        nombre_archivo = os.path.basename(source_file_path)
        mensaje_archivo = f'Archivo copiado {nombre_archivo}'
    else: 
        mensaje_archivo = f'El archivo {source_file_path} no existe o cambio de ubicación'
        
    # Mostrar mensaje emergente con el resultado
    mensaje_final = f"{mensaje_carpeta}\n{mensaje_archivo}"
    messagebox.showinfo("Resultado", mensaje_final)
        
        
if __name__ == '__main__':
    main()