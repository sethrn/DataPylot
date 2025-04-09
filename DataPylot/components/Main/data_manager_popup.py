import tkinter as tk
from tkinter import ttk, filedialog, messagebox

class DataFrameManagerPopup(tk.Toplevel):
    def __init__(self, parent, session_data):
        super().__init__(parent)
        self.title("Manage DataFrames")
        self.session = session_data
        self.geometry("500x500")
        self.resizable(False, True)
        self.center_popup(parent.master.master.master.top_pane)
        self.parent = parent

        self.frame_container = ttk.Frame(self)
        self.frame_container.grid(row=0, column=0, padx=0, pady=20, sticky="nsew")

        self.close_btn = ttk.Button(self, command=self.on_close_selected, text="Close")
        self.close_btn.grid(row=1, column=0, padx=0, pady=20, sticky="s")
        self.protocol("WM_DELETE_WINDOW", self.on_close_selected)

        self.frame_container.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.refresh_frame_list()

        self.transient(parent)
        self.grab_set()
        
        self.wait_window(self)

    def on_close_selected(self):
        self.parent.master.master.master.main_stage.refresh_children()
        self.destroy()
        

    def refresh_frame_list(self):
        for widget in self.frame_container.winfo_children():
            widget.destroy()

        for i, df_name in enumerate(self.session.getDFNames()):
            label = ttk.Label(self.frame_container, text=df_name, font=("Arial", 8))
            label.grid(row=i, column=0, padx=(30,0), pady=5, sticky="w")

            rename_btn = ttk.Button(
                self.frame_container,
                text="Rename",
                command=lambda n=df_name: self.rename_dataframe(n)
            )
            rename_btn.grid(row=i, column=0, padx=(200,0), pady=5, sticky="w")

            delete_btn = ttk.Button(
                self.frame_container,
                text="Delete",
                command=lambda n=df_name: self.delete_dataframe(n)
            )
            delete_btn.grid(row=i, column=0, padx=(400,0), pady=5, sticky="w")

            download_btn = ttk.Button(
                self.frame_container,
                text="Download",
                command=lambda n=df_name: self.download_dataframe(n)
            )
            download_btn.grid(row=i, column=0, padx=(275,0), pady=5, sticky="w")

    def rename_dataframe(self, old_name):
        row_index = self.session.getDFNames().index(old_name)

        for widget in self.frame_container.grid_slaves(row=row_index):
            widget.destroy()

        entry = ttk.Entry(self.frame_container)
        entry.insert(0, old_name)
        entry.grid(row=row_index, column=0, padx=5, pady=5)

        confirm_btn = ttk.Button(
            self.frame_container,
            text="Confirm",
            command=lambda: self.apply_rename(old_name, entry.get().strip())
        )
        confirm_btn.grid(row=row_index, column=1, padx=5, pady=5)

        cancel_btn = ttk.Button(
            self.frame_container,
            text="Cancel",
            command=self.refresh_frame_list
        )
        cancel_btn.grid(row=row_index, column=2, padx=5, pady=5)

    def apply_rename(self, old_name, new_name):
        if not new_name or new_name == old_name:
            self.refresh_frame_list()
            return

        if new_name in self.session.getDFNames():
            messagebox.showerror("Rename Failed", f"A DataFrame named '{new_name}' already exists.")
            return

        df_obj = self.session.getDataFrame(old_name)
        self.session.deleteDataFrame(old_name)
        self.session.DataFrames[new_name] = df_obj
        self.refresh_frame_list()

    def delete_dataframe(self, name):
        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?")
        if confirm:
            self.session.deleteDataFrame(name)
            self.refresh_frame_list()

    def download_dataframe(self, name):
        df = self.session.getDataFrame(name)
        if df is not None:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title=f"Save '{name}' as..."
            )
            if file_path:
                try:
                    df.to_csv(file_path, index=False)
                    messagebox.showinfo("Download Complete", f"DataFrame '{name}' saved successfully.")
                except Exception as e:
                    messagebox.showerror("Download Failed", str(e))

    def center_popup(self, parent):
        self.update_idletasks() 

        width = self.winfo_width()
        height = self.winfo_height()

        x = parent.winfo_rootx() + (parent.winfo_width() - width) // 2
        y = parent.winfo_rooty() + (parent.winfo_height() - height) // 2

        self.geometry(f"{width}x{height}+{x}+{y}")
