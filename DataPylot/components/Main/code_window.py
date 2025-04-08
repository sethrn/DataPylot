import tkinter as tk
from tkinter import ttk

from components.Patterns.popup_dialog import PopupDialog

class CodeWindow(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
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

        self.undo_btn = ttk.Button(
            self.actions_frame,
            text="Undo Operation",
            command=self.undo_code,
            state="disabled"
        )
        self.undo_btn.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="ew")

        self.delete_btn = ttk.Button(
            self.actions_frame,
            text="Delete Code Snippet",
            command=self.delete_code,
            state="disabled"
        )
        self.delete_btn.grid(row=4, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
     
    def onCodeAdded(self, index):
        self.index = index
        self.updateWindow()

    def updateWindow(self):
        self.len = self.winfo_toplevel().SessionData.getOutputsLength()

        if self.index >= self.len:
            self.index = max(0, self.len - 1)

        code = self.winfo_toplevel().SessionData.getOutput(self.index)
        isUndoable = self.winfo_toplevel().SessionData.canUndo(self.index)

        self.output_text.config(state="normal")
        self.output_text.delete("1.0", tk.END)
        if code:
            self.output_text.insert("1.0", code)
        self.output_text.config(state="disabled")

        self.prev_btn.config(state="normal" if self.index > 0 else "disabled")
        self.next_btn.config(state="normal" if self.index < self.len - 1 else "disabled")
        self.copy_btn.config(state="normal" if self.len > 0 else "disabled")
        self.undo_btn.config(state="normal" if isUndoable else "disabled")
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

    def undo_code(self):
        df_name = self.winfo_toplevel().SessionData.getUndoableDataFrameAtIndex(self.index)
        if df_name:
            confirm_popup = PopupDialog(
                self,
                title="Undo DataFrame Change",
                message=f"Are you sure you want to undo the most recent change to '{df_name}'?",
                on_right=lambda: self.perform_undo(df_name),
                on_left=lambda: self.focus_set(),  # just regain focus
                rightButton="Yes",
                leftButton="Cancel"
            )
            confirm_popup.center_popup(self.parent.master.master.top_pane)

    def perform_undo(self, df_name):
        self.winfo_toplevel().SessionData.undoDataFrameChange(df_name)
        self.delete_code()

    def delete_code(self):
        self.winfo_toplevel().SessionData.deleteOutput(self.index)

        if self.index >= self.winfo_toplevel().SessionData.getOutputsLength():
            self.index = max(0, self.index - 1)

        self.updateWindow()
