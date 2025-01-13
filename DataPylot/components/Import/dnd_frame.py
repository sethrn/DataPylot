import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

class DnDFrame(ttk.Frame):
    def __init__(self, parent, id_frame_ref):
        super().__init__(parent)

        self.id_frame = id_frame_ref

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        style = ttk.Style()
        style.configure(
            "DnDFrame.TFrame", 
            background="lightgray", 
            relief="groove", 
            borderwidth=2
        )

        self.grid_propagate(False)
        self["style"] = "DnDFrame.TFrame"

        self.config(width=250, height=250)

        self.label1 = ttk.Label(
            self, 
            text="Drag & Drop A File", 
            font=("Arial", 12), 
            anchor="center",
            background="lightgray"
        )
        self.label1.grid(row=0, column=0, sticky="nsew", padx=10, pady=5)

        self.browse_btn = ttk.Button(self, text="Browse Files", command=self.browse_files)
        self.browse_btn.grid(row=1, column=0, sticky="nsew", padx=10, pady=5)

        self.label2 = ttk.Label(
            self,
            text="Accepted File formats: .csv,.tsv,.txt,.xslx,.json",
            font=("Arial", 8),
            anchor="center",
            background="lightgray"
        )
        
        self.label2.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)

    def browse_files(self):
        file_path = filedialog.askopenfilename(
            title="Select a File",
            filetypes=[
                ("CSV Files", "*.csv"), 
                ("TSV Files", "*.tsv"),
                ("Text Files", "*.txt"),
                ("Excel Files", "*.xlsx"),
                ("JSON Files", "*.json")
            ]
        )
        if file_path:
            self.id_frame.validate_file(type("Event", (object,), {"data": file_path}))