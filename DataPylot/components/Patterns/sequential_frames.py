import tkinter as tk
from tkinter import ttk

class SequentialFrameManager(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.frames = []
        self.current_idx = 0

        self.params = {}

        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        self.nav_frame = ttk.Frame(self)
        self.nav_frame.pack(side="bottom", fill="x", pady=10)

        self.back_btn = ttk.Button(self.nav_frame, text="Back", command=self.prev_frame)
        self.next_btn = ttk.Button(self.nav_frame, text="Next", command=self.next_frame)
        self.next_btn.pack(side="right", padx=5)
        self.back_btn.pack(side="right", padx=5)


    def add_frame(self, frame_class, manager=None):
        if manager:
            frame = frame_class(self.content_frame, manager)
        else:
            frame = frame_class(self.content_frame)
        self.frames.append(frame)

    def show_frame(self, index):
        if 0 <= index < len(self.frames):
            for frame in self.frames:
                frame.place_forget()

            self.frames[index].place(relwidth=1, relheight=1)
            self.current_index = index

            self.back_btn.config(state="normal" if index > 0 else "disabled")
            self.next_btn.config(state="normal" if index < len(self.frames)-1 else "disabled")

    def next_frame(self):
        if self.current_index < len(self.frames) - 1:
            self.show_frame(self.current_index + 1)

    def prev_frame(self):
        if self.current_index > 0:
            self.show_frame(self.current_index - 1)

    def clear_frames(self):
        for frame in self.frames:
            for widget in frame.winfo_children():
                if isinstance(widget, ttk.Entry):
                    widget.delete(0, tk.END)
                elif isinstance(widget, ttk.Combobox):
                    widget.set("")
                elif isinstance(widget, ttk.CheckButton):
                    widget.deselect()
                elif isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)

    def delete_frame_by_index(self, index):
        if 0 <= index < len(self.frames):
            frame = self.frames.pop(index)
            frame.destroy()

    def delete_current_frame(self):
        frame = self.frames.pop(self.current_idx)
        frame.destroy()
        self.current_idx -= 1