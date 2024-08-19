import customtkinter as ctk
import tkinter as tk
from gui_settings import *
#In case it run on MacOs
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


#Main Application
#The main application has a in-built autor label at the bottom
class Application(ctk.CTk):
    def __init__(self, geometry: tuple, title = "Rothmain"):
        super().__init__(fg_color=GREEN)
        self.geometry(f"{geometry[0]}x{geometry[1]}")
        self.title("")
        self.resizable(False, False)
        # self.iconbitmap("empty.ico")
        
        #Title color 
        HWND = windll.user32.GetParent(self.winfo_id())
        title_bar_color = TITLE_COLOR
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, 
            35,
            byref(c_int(title_bar_color)),
            sizeof(c_int)
            )
        
        autor_label = ctk.CTkLabel(
            self, 
            text="Design by Carlos Rothmann La Luz ", 
            text_color=GRAY, 
            font=AUX_TEXT
            )
        autor_label.pack(side="bottom")   
#Wigets   

class Confirmation_Button(ctk.CTkButton):
    def __init__(self, parent, button_text, func):
        super().__init__(master= parent, text=button_text, command=func, fg_color=BLACK, font=MAIN_TEXT_B) 
        
        
        self.pack(
        side="bottom", 
        pady= 5, 
        padx= 5, 
        anchor="s"
        ) 
        
class Entry_Segment(ctk.CTkFrame):
    def __init__(self, parent, label_text, var, advice):
        super().__init__(master=parent, fg_color=GREEN)
        
        # Single column layout with 3 rows
        self.columnconfigure((0), weight=1) 
        self.rowconfigure((0,1,2,), weight=1, uniform="c")  
        
        padx = 10
        pady = 0
        
        #Frame placing
        
        self.pack(expand = False, fill="x", pady=1)
        
        #Label
        ctk.CTkLabel(self, text=label_text, font=MAIN_TEXT).grid(
            row=0, 
            column=0, 
            sticky="sw", 
            padx=padx, 
            pady=pady,
            )
        
        #Entry
        
        ctk.CTkEntry(self, textvariable=var, font=MAIN_TEXT).grid(
            row=1, 
            column=0, 
            sticky="ew", 
            padx=padx, 
            pady=pady,
            )

        #Advice
        ctk.CTkLabel(self, text=advice, text_color=GRAY, font=AUX_TEXT).grid(
            row=2, 
            column=0, 
            sticky="nw", 
            padx=padx, 
            pady=2,
            )

class Dropdown_Segment(ctk.CTkFrame):
    def __init__(self, parent, label_text, option_list, option, advice):
        super().__init__(master=parent, fg_color=GREEN)
        
        # Single column layout with 3 rows
        self.columnconfigure((0), weight=1) 
        self.rowconfigure((0,1,2,), weight=1, uniform="c")  
        
        padx = 10
        pady = 0
        
        #Frame placing
        
        self.pack(expand = False, fill="x", pady=1)
        
        #Label
        ctk.CTkLabel(self, text=label_text, font=MAIN_TEXT).grid(
            row=0, 
            column=0, 
            sticky="nw", 
            padx=padx, 
            pady=pady,
            )
        
        #DropDown
        
        dropdown = ctk.CTkComboBox(
            self, 
            values=option_list, 
            variable = option, 
            font=MAIN_TEXT
                )
        dropdown.grid(
                    row=1, 
                    column=0, 
                    sticky="ew", 
                    padx=padx, 
                    pady=pady,
                    )
        dropdown.set(option_list[0])

        #Advice
        ctk.CTkLabel(
            self, text=advice, text_color=GRAY, font=AUX_TEXT
            ).grid(
                row=2, 
                column=0, 
                sticky="sw", 
                padx=padx, 
                pady=2,
                )
   
def main():
    
    PROJECT_TIPES = [
    "Residencial",
    "Educativo",
    "Sanitario",
    "Oficinas",
    "Paisajismo",
    "Transporte",
    "MasterPlan",
    "Recreativo",
    "Interiorismo",
]

    app = Application((300, 450), "Project Creator")
    
    
    project_string = tk.StringVar()
    Entry_Segment(
        app, 
        "NOMBRE Project:", 
        project_string,
        "Ejem: VivendaPlurifamiliar Mataro"
        )
    
    dropdown_string = tk.StringVar()
    Dropdown_Segment(app,
                     "Project Type",
                     PROJECT_TIPES, 
                     dropdown_string,
                     "En caso de mas de un tipo elegir el principal"
                     )
    
    Entry_Segment(
        app, 
        "Client:", 
        project_string,
        "Ejem: VivendaPlurifamiliar Mataro"
        )
    
    Entry_Segment(
        app, 
        "UBICACION:", 
        project_string,
        "Ejem: VivendaPlurifamiliar Mataro"
        )
    
    Confirmation_Button(app, "Crear projecto", lambda: print("hello world")).pack(side="bottom")
    
    app.mainloop()

if __name__ == "__main__":
    main() 