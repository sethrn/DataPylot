import tkinter as tk
from tkinter import ttk

class CodeWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.index = 0
        self.len = 0

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.output_text = tk.Text(
            self,
            wrap="word",
            height=15,
            state="disabled",
            font=("Courier", 10)
        )
        self.output_text.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.actions_frame = ttk.Frame(self)
        self.actions_frame.grid(row=0, column=1, sticky="ne", padx=5, pady=5)

        self.top_label = ttk.Label(self.actions_frame, text="Code Output Window")
        self.top_label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.prev_btn = ttk.Button(self.actions_frame, text="Previous", command=self.prev_output, state="disabled")
        self.next_btn = ttk.Button(self.actions_frame, text="Next", command=self.next_output, state="disabled")
        
        self.prev_btn.grid(row=1, column=0, padx=5, pady=5)
        self.next_btn.grid(row=1, column=1, padx=5, pady=5)

        self.copy_btn = ttk.Button(
            self.actions_frame,
            text="Copy Code",
            command=self.copy_code,
            state="disabled"
        )
        self.copy_btn.grid(row=2, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        self.delete_btn = ttk.Button(
            self.actions_frame,
            text="Delete Code Snippet",
            command=self.delete_code,
            state="disabled"
        )
        self.delete_btn.grid(row=3, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
     
    def onCodeAdded(self, index):
        if index >= 0:
            self.len = index+1
            self.index = index
        else:
            self.len = 1
            self.index = 0
        self.updateWindow()

    def updateWindow(self):
        code = self.winfo_toplevel().SessionData.getOutput(self.index)
        if code:
            self.output_text.config(state="normal")
            self.output_text.delete("1.0", tk.END)
            self.output_text.insert("1.0", code)
            self.output_text.config(state="disabled")

        self.prev_btn.config(state="normal" if self.index > 0 else "disabled")
        self.next_btn.config(state="normal" if self.index < self.len-1 else "disabled")
        self.copy_btn.config(state="normal" if self.len > 0 else "disabled")
        self.delete_btn.config(state="normal" if self.len > 0 else "disabled")

    def prev_output(self):
        if self.index > 0:
            self.index -= 1
            self.updateWindow()

    def next_output(self):
        if self.index < self.len-1:
            self.index += 1
            self.updateWindow()

    def copy_code(self):
        code = self.winfo_toplevel().SessionData.getOutput(self.index)
        if code:
            self.clipboard_clear()
            self.clipboard_append(code)

    def delete_code(self):
        self.winfo_toplevel().SessionData.deleteOutput(self.index)

        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state="disabled")

        self.len -= 1
        if self.index > 0:
            self.index -= 1
        self.updateWindow()
