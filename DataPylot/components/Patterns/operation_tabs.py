from tkinter import ttk

class OperationTabFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)
        self.notebook.bind("<<NotebookTabChanged>>", lambda e: self.on_tab_changed())
        self.tab_configs = []

    def add_tab(self, frame_class, tab_title):
        frame = frame_class(self.notebook)
        self.notebook.add(frame, text=tab_title)
        self.tab_configs.append((frame_class, tab_title))

    def on_tab_changed(self):
        selected_id = self.notebook.select()
        selected_tab = self.nametowidget(selected_id)
        tab_text = self.notebook.tab(selected_id, "text")

        if hasattr(selected_tab, "notebook"):
            inner_notebook = selected_tab.notebook
            inner_selected_id = inner_notebook.select()
            tab_text = inner_notebook.tab(inner_selected_id, "text")
    
        self.winfo_toplevel().SessionData.setAboutStep(tab_text)

    def refresh_children(self):
        current_tab_id = self.notebook.select()
        current_tab_idx = self.notebook.index(current_tab_id)

        current_frame = self.nametowidget(current_tab_id)
        inner_tab_idx = None

        for tab_id in self.notebook.tabs():
            self.notebook.forget(tab_id)

        for frame_class, tab_title in self.tab_configs:
            new_frame = frame_class(self.notebook)
            self.notebook.add(new_frame, text=tab_title)

        if 0 <= current_tab_idx < self.notebook.index("end"):
            self.notebook.select(current_tab_idx)