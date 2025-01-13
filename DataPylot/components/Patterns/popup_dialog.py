import tkinter as tk
from tkinter import ttk

class PopupDialog(tk.Toplevel):
    def __init__(self, parent, title, message, on_left, on_right, rightButton=None, leftButton=None, modal=True):
        super().__init__(parent)
        self.title(title)
        self.configure(bg="white")

        message_label = ttk.Label(
            self, 
            text=message, 
            font=("Arial", 12), 
            background="white", 
            anchor="center"
        )
        message_label.pack(pady=15, padx=20)

        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(pady=(20, 10), padx=10, fill="x")

        if rightButton:
            right_btn = ttk.Button(
                button_frame, text=rightButton, command=lambda: self._handle_action(on_right)
            )
            right_btn.pack(side="right", padx=5)
        
        if leftButton:
            left_btn = ttk.Button(
                button_frame, text=leftButton, command=lambda: self._handle_action(on_left)
            )
            left_btn.pack(side="left", padx=5)

        if modal:
            self.transient(parent)
            self.grab_set()

        self.center_popup(parent)


    def _handle_action(self, action):
        if callable(action):
            action()
        self.destroy()

    def center_popup(self, parent):
        self.update_idletasks() 

        width = self.winfo_width()
        height = self.winfo_height()

        x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")