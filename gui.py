import customtkinter as ctk
from tkinter import simpledialog, filedialog, messagebox
from ctypes import windll, byref, sizeof, c_int

#Main Application
#The main application has a in-built autor label at the bottom
class Application(ctk.CTk):
    def __init__(self, geometry: tuple, title = "Rothmain", *args):
        super().__init__()
        self.geometry(f"{geometry[0]}x{geometry[1]}")
        self.title(title)
        
        autor_label = ctk.CTkLabel(self, text="Design by Carlos Rothmann La Luz")
        autor_label.pack(side="bottom")
        
        #Title color 
        HWND = windll.user32.GetParent(self.winfo_id())
        title_bar_color = 0x544343
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, 
            35,
            byref(c_int(title_bar_color)),
            sizeof(c_int)
            )
            
#Wigets   
        
class Dropdown(ctk.CTkComboBox):
    def __init__(self, parent):
        super().__init__(parent)
        pass  

class Confirmation_Button(ctk.CTkButton):
    def __init__(self, parent, button_text):
        super().__init__(parent, text=button_text)
        self.pack()

class Status_Box(ctk.CTkLabel):
    def __init__(self, parent, status):
        super().__init(parent, text=status)
        self.pack
        
   
def main():
    app = Application((500, 500), "Rothmain")

    
    app.mainloop()

if __name__ == "__main__":
    main() 