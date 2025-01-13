from tkinter import ttk

class OperationTabFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

    def add_tab(self, frame_class, tab_title):
        frame = frame_class(self.notebook)
        self.notebook.add(frame, text=tab_title)
        

