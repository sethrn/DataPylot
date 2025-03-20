import tkinter as tk
from tkinter import ttk
import re
from pathlib import Path
import sys
from TkinterDnD2 import DND_FILES

from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.popup_dialog import PopupDialog
from components.Import.dnd_frame import DnDFrame
from CodeGenerators.Imports.gen_import import ImportGenerator

class IDFrame(GenerateCodeFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.file_path = ""
        self.colab_mode = tk.BooleanVar(value=False)

        if hasattr(sys, '_MEIPASS'):
            base_dir = Path(sys._MEIPASS)
        else:
            base_dir = Path(__file__).resolve().parent.parent.parent
        
        about_path = base_dir / "edu" / "Import" / "about.txt"

        self.winfo_toplevel().SessionData.setAboutStep(str(about_path))
        
        self.drop_target_register(DND_FILES)
        self.dnd_bind("<<Drop>>", self.validate_file)

        top_label = ttk.Label(self.content_frame, text="Import A Dataset", font=("Arial", 14))
        top_label.grid(row=0, column=0, padx=10, pady=(20,5), sticky="n")

        self.dnd_frame = DnDFrame(self.content_frame, id_frame_ref=self)
        self.dnd_frame.grid(row=1, column=0, padx=10, pady=5, sticky="n")

        self.fp_label = ttk.Label(self.content_frame, text="File Path:", font=("Arial", 10))
        self.fp_label.grid(row=2, column=0, padx=5, pady=5, sticky="n")
        
        name_label = ttk.Label(self.content_frame, text="Enter DataFrame name:")
        name_label.grid(row=3, column=0, padx=5, pady=5, sticky="nw")

        self.name_entry = ttk.Entry(self.content_frame, width=30)
        self.name_entry.grid(row=3, column=0, padx=(140, 5), pady=5, sticky="nw")

        rows_label = ttk.Label(self.content_frame, text="Display first")
        rows_label.grid(row=4, column=0, padx=(5,5), pady=5, sticky="nw")

        self.rows_entry = ttk.Entry(self.content_frame, width=5)
        self.rows_entry.insert(0, "5")
        self.rows_entry.grid(row=4, column=0, padx=(70, 5), pady=5, sticky="nw")

        rows_suffix_label = ttk.Label(self.content_frame, text="rows")
        rows_suffix_label.grid(row=4, column=0, padx=(105,5), pady=5, sticky="nw")

        self.colab_checkbox = ttk.Checkbutton(
            self.content_frame,
            text="Using Google Colab",
            variable=self.colab_mode
        )
        self.colab_checkbox.grid(row=5, column=0, padx=5, pady=5, sticky="nw")

        self.content_frame.grid_columnconfigure(0, weight=1)

        self.content_frame.grid_columnconfigure(0, weight=1)  

        self.reset_inputs()

    def validate_file(self, event):
        file_path = event.data.strip()
        suffixes = (".txt", ".csv", ".tsv", ".xlsx", ".json")

        if file_path.endswith(suffixes):
            self.fp_label.config(
                text=f"File Path: {file_path}",
                foreground="black"
            )
            self.generate_btn.config(state="normal")
            self.file_path = file_path
        else:
            self.fp_label.config(
                text=f"File Path: {file_path} is not an accepted format",
                foreground="red"
            )
            self.generate_btn.config(state="disabled")

            self.file_path = ""

    def validate_name(self, name):
        return re.match(r"^[A-Za-z]\w*$", name) is not None

    def validate_rows(self, rows):
        try:
            rows = int(rows)
            return rows > 0
        except ValueError:
            return False

    def generate_code(self):
        name = self.name_entry.get().strip()
        rows = self.rows_entry.get().strip()
        colab_mode = self.colab_mode.get()

        if not self.validate_rows(rows):
            self.fp_label.config(
                text="Error: Rows must be a positive integer.", 
                foreground="red"
            )
            return

        if not self.validate_name(name):
            self.fp_label.config(
                text="Error: Invalid dataset name. Please use only letters, numbers, and underscores. The name must start with a letter.",
                foreground="red"
            )
            return

        existing_names = self.winfo_toplevel().SessionData.getDFNames()

        if name in set(existing_names):
            self.open_overwrite_popup(name, rows, colab_mode)
            return
        self.finalize_code_generation(name, rows, colab_mode)


    def open_overwrite_popup(self, name, rows, colab_mode):
        PopupDialog(
            self,
            title="Duplicate DataFrame Name",
            message=f"A DataFrame named '{name}' already exists.\nDo you want to overwrite it?",
            on_right=lambda: self.finalize_code_generation(name, rows, colab_mode),
            on_left=lambda: self.fp_label.config(text="Action cancelled.", foreground="black"),
            rightButton="Yes",
            leftButton="No"
        )

    def finalize_code_generation(self, name, rows, colab_mode):
        status = self.winfo_toplevel().SessionData.TryAddDataFrame(name, self.file_path)

        if status == 1:
            self.fp_label.config(text=f"File successfully loaded as DataFrame '{name}'", foreground="green")
        else:
            self.fp_label.config(text="Error: Could not load the file.", foreground="red")
        
        with_import = self.include_import_var.get()
        code, imports = ImportGenerator.generate(self.file_path, name, rows, with_import, colab_mode)
        
        if code:
            self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.reset_inputs()

    def reset_inputs(self):
        self.name_entry.delete(0, tk.END)
        self.rows_entry.delete(0, tk.END)
        self.rows_entry.insert(0, "5")
        self.generate_btn.config(state="disabled")
        self.file_path = ""
        self.colab_mode.set(False)