import customtkinter as ctk
from gui_settings import *
from tkinter import ttk, messagebox, simpledialog
import json

# In case it run on MacOs
try:
    from ctypes import windll, byref, sizeof, c_int
except:
    pass


# Main Application
# The main application has a in-built autor label at the bottom
class Application(ctk.CTk):
    def __init__(self, geometry: tuple, title=""):
        super().__init__(fg_color=GREEN)
        self.geometry(f"{geometry[0]}x{geometry[1]}")
        self.title(title)
        self.resizable(False, False)
        # self.iconbitmap("empty.ico")

        # Title color
        HWND = windll.user32.GetParent(self.winfo_id())
        title_bar_color = TITLE_COLOR
        windll.dwmapi.DwmSetWindowAttribute(
            HWND, 35, byref(c_int(title_bar_color)), sizeof(c_int)
        )

        autor_label = ctk.CTkLabel(
            self,
            text="Design by Carlos Rothmann La Luz ",
            text_color=GRAY,
            font=AUX_TEXT,
        )
        autor_label.pack(side="bottom")


# Wigets


class Confirmation_Button(ctk.CTkButton):
    def __init__(self, parent, button_text, func):
        super().__init__(
            master=parent,
            text=button_text,
            command=func,
            fg_color=DARK_GREEN,
            font=MAIN_TEXT_B,
        )

        self.pack(side="bottom", pady=5, padx=5, anchor="s")


class Entry_Segment(ctk.CTkFrame):
    def __init__(self, parent, label_text, var, advice):
        super().__init__(master=parent, fg_color=GREEN)

        # Single column layout with 3 rows
        self.columnconfigure((0), weight=1)
        self.rowconfigure(
            (
                0,
                1,
                2,
            ),
            weight=1,
            uniform="c",
        )

        padx = 10
        pady = 0

        # Frame placing

        self.pack(expand=False, fill="x", pady=1)

        # Label
        ctk.CTkLabel(self, text=label_text, font=MAIN_TEXT).grid(
            row=0,
            column=0,
            sticky="sw",
            padx=padx,
            pady=pady,
        )

        # Entry

        ctk.CTkEntry(self, textvariable=var, font=MAIN_TEXT).grid(
            row=1,
            column=0,
            sticky="ew",
            padx=padx,
            pady=pady,
        )

        # Advice
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
        self.rowconfigure(
            (
                0,
                1,
                2,
            ),
            weight=1,
            uniform="c",
        )

        padx = 10
        pady = 0

        # Frame placing

        self.pack(expand=False, fill="x", pady=1)

        # Label
        ctk.CTkLabel(self, text=label_text, font=MAIN_TEXT).grid(
            row=0,
            column=0,
            sticky="nw",
            padx=padx,
            pady=pady,
        )

        # DropDown

        dropdown = ctk.CTkComboBox(
            self, values=option_list, variable=option, font=MAIN_TEXT
        )
        dropdown.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=padx,
            pady=pady,
        )
        dropdown.set(option_list[0])

        # Advice
        ctk.CTkLabel(self, text=advice, text_color=GRAY, font=AUX_TEXT).grid(
            row=2,
            column=0,
            sticky="sw",
            padx=padx,
            pady=2,
        )


class Tab(ctk.CTkTabview):
    def __init__(self, parent: str, geometry: tuple):
        super().__init__(
            master=parent,
            width=geometry[0],
            height=geometry[1],
            fg_color=GREEN,
            segmented_button_fg_color=GREEN,
            segmented_button_selected_color=DARK_GREEN,
            segmented_button_selected_hover_color=DARK_GREEN,
        )

        self.pack()
        self.add("Create")
        self.add("Settings")
        self.add("Dir Structure")


class Setting_button(ctk.CTkFrame):
    def __init__(self, parent, label_text, path, button_text, func):
        super().__init__(master=parent, fg_color=GREEN)

        # Single column layout with 3 rows
        self.columnconfigure((0), weight=1)
        self.rowconfigure(
            (
                0,
                1,
                2,
            ),
            weight=1,
            uniform="c",
        )

        padx = 10
        pady = 0

        # Frame placing

        self.pack(expand=False, fill="x", pady=1)

        # Label
        ctk.CTkLabel(self, text=label_text, font=MAIN_TEXT).grid(
            row=0,
            column=0,
            sticky="sw",
            padx=padx,
            pady=pady,
        )

        # Entry

        ctk.CTkLabel(
            self,
            textvariable=path,
            wraplength=350,
            justify="left",
            font=MAIN_TEXT,
            fg_color=WHITE,
            anchor="w",
            corner_radius=5,
        ).grid(
            row=1,
            column=0,
            sticky="ew",
            padx=padx,
            pady=pady,
        )

        # Advice
        ctk.CTkButton(
            self, text=button_text, font=MAIN_TEXT_B, fg_color=DARK_GREEN, command=func
        ).grid(
            row=2,
            column=0,
            sticky="nw",
            padx=padx,
            pady=2,
        )


class Folder_Struc(ctk.CTkFrame):
    def __init__(self, parent, json_file):
        super().__init__(master=parent, fg_color=GREEN)

        with open(json_file, 'r') as file:
            self.json_data = json.load(file)
            self.folder_structure = self.json_data.get("folder_structure")
        
        self.pack(fill='both', expand=True)
        
        # Editing Buttons
        button_frame = ctk.CTkFrame(self, fg_color=GREEN)
        button_frame.pack(fill='x', pady=1)

        add_button = ctk.CTkButton(
            button_frame, 
            text="Add Folder", 
            fg_color=DARK_GREEN,
            command=lambda: self.add_folder()
            )
        add_button.pack(side='left', padx=5)

        remove_button = ctk.CTkButton(
            button_frame, 
            text="Remove Folder", 
            fg_color=DARK_GREEN,
            command=lambda: self.remove_folder()
            )
        remove_button.pack(side='left', padx=5)
        
        # Treeview
        tree_frame = ctk.CTkFrame(self, fg_color=GREEN)
        tree_frame.pack(fill='both', pady=1)
        
        self.tree = ttk.Treeview(tree_frame)
        self.tree.pack(side= "left", fill='both', expand=True)

        self.scrollbar = ctk.CTkScrollbar(
            tree_frame, 
            orientation="vertical", 
            command=self.tree.yview
            )
        self.scrollbar.pack(side='right', fill='y')
        self.tree.configure(yscrollcommand=self.scrollbar.set)

        # Populate the Treeview with the folder structure
        self.populate_treeview('', self.folder_structure)
        
        
        # Save changes to the folder structure button
        save_button = ctk.CTkButton(
            self, 
            text="Save Changes", 
            fg_color=DARK_GREEN,
            command= lambda: self.save_json(json_file)
            )
        save_button.pack(side='bottom', pady=10)


    def populate_treeview(self, parent, structure):
        for folder, subfolders in structure.items():
            folder_id = self.tree.insert(parent, 'end', text=folder)
            if isinstance(subfolders, list):
                for subfolder in subfolders:
                    self.tree.insert(folder_id, 'end', text=subfolder)
            elif isinstance(subfolders, dict):
                self.populate_treeview(folder_id, subfolders)
             
             
    def add_folder(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a folder to add a subfolder.")
            return

        parent_id = selected_item[0]
        folder_name = simpledialog.askstring("Folder Name", "Enter the new folder name:")
        if not folder_name:
            return
        
        self.tree.insert(parent_id, 'end', text=folder_name.upper())


    def remove_folder(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a folder to remove.")
            return

        folder_id = selected_item[0]
        folder_name = self.tree.item(folder_id, "text")

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the folder '{folder_name}'?")
        if not confirm:
            return

        self.tree.delete(folder_id)


    def get_tree_data(self, tree, item=""):
        data = {}
        tree_data = tree.get_children(item)
        for branch in tree_data:
            item_text = tree.item(branch)["text"]
            subranch = tree.get_children(branch)
            if subranch:
                data[item_text] = self.get_tree_data(tree, branch)
            else:
                if item in data:
                    data[item].append(item_text)
                else:
                    data[item_text] = []
        return data


    def save_json(self, file_path):
        settings = self.json_data
        data = self.get_tree_data(self.tree)
        settings["folder_structure"] = data

        try:
            with open(file_path, 'w') as f:
                json.dump(settings, f, indent=4)
                messagebox.showinfo("OK","New directory structure save")
        except Exception as error:
            messagebox.showwarning("Error", f"An error ocurred: {error}")
              


def main():
    pass

if __name__ == "__main__":
    main()
