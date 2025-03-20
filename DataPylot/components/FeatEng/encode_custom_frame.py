import tkinter as tk
from tkinter import ttk
import re

from CodeGenerators.FeatEng.gen_exe_encodecustom import EncodeCustomExecutor
from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.popup_dialog import PopupDialog

class EncodeCustomFrame(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.df_name = self.manager.params["df"]
        self.feature = self.manager.params["feature"]

        self.group_names = []
        self.group_values = []
        self.current_group_idx = -1
        self.ungrouped_values = set()

        df = self.winfo_toplevel().SessionData.getDataFrame(self.df_name)
        if df is not None:
            self.ungrouped_values = set(df[self.feature].dropna().unique())
            self.feat_dtype = df[self.feature].dtype

        top_label = ttk.Label(self, text="Customize Encoding by Grouping Values", font=("Arial", 14))
        top_label.grid(row=0, column=0, padx=5, pady=(20, 5), sticky="n")

        self.create_group_btn = ttk.Button(self, text="Create Encoding Group", command=self.on_create_group_btn)
        self.create_group_btn.grid(row=1, column=0, padx=(75, 5), pady=(30, 15), sticky="w")

        self.err_label = ttk.Label(self, text="Test", font=("Arial", 10), foreground="red")
        #self.err_label.grid(row=1, column=0, padx=5, pady=(465, 5), sticky="w")

        ungrouped_label = ttk.Label(self, text="Remaining Values:", font=("Arial", 10))
        ungrouped_label.grid(row=2, column=0, padx=(75, 5), pady=(5, 5), sticky="w")

        self.group_label = ttk.Label(self, text="Current Encoding:", font=("Arial", 10))
        self.group_label.grid(row=2, column=0, padx=(325, 5), pady=(5, 5), sticky="w")

        self.ungrouped_listbox = tk.Listbox(self, selectmode="extended", height=10, width=30)
        self.ungrouped_listbox.grid(row=3, column=0, padx=(75, 5), pady=(5, 5), sticky="w")

        self.grouped_listbox = tk.Listbox(self, selectmode="extended", height=10, width=30)
        self.grouped_listbox.grid(row=3, column=0, padx=(325, 5), pady=(5, 5), sticky="w")

        self.ungrouped_listbox.bind("<<ListboxSelect>>", lambda e: self.on_select_ungrouped())
        self.grouped_listbox.bind("<<ListboxSelect>>", lambda e: self.on_select_grouped())

        for value in set(sorted(self.ungrouped_values)):
            self.ungrouped_listbox.insert(tk.END, value)

        btn_frame = ttk.Frame(self)
        btn_frame.grid(row=3, column=0, padx=(525, 5), pady=(5, 5), sticky="w")

        self.prev_btn = ttk.Button(btn_frame, text="Previous Group", width=14, state="disabled", command=self.on_prev_btn)
        self.prev_btn.pack(pady=(0, 10))

        self.next_btn = ttk.Button(btn_frame, text="Next Group", width=14, state="disabled", command=self.on_next_btn)
        self.next_btn.pack(pady=(0, 50))

        self.delete_group_btn = ttk.Button(btn_frame, text="Delete Group", width=14, state="disabled", command=self.on_delete_btn)
        self.delete_group_btn.pack()

        self.assign_btn = ttk.Button(self, text="Assign to Group", state="disabled", command=self.on_assign_btn)
        self.assign_btn.grid(row=4, column=0, padx=(120, 5), pady=(10, 5), sticky="w")

        self.remove_btn = ttk.Button(self, text="Remove from Group", state="disabled", command=self.on_remove_btn)
        self.remove_btn.grid(row=4, column=0, padx=(360, 5), pady=(10, 5), sticky="w")

        self.finish_btn = ttk.Button(self, text="Finish", width=20, state="disabled", command=self.on_finish_button)
        self.finish_btn.grid(row=5, column=0, padx=5, pady=(10, 5), sticky="n")

        self.grid_columnconfigure(0, weight=1)

    def on_create_group_btn(self):
        self.create_group_btn.destroy()
            
        self.set_group_label = ttk.Label(self, text="Set Encoding Value:", font=("Arial", 10))
        self.set_group_label.grid(row=1, column=0, padx=(75, 5), pady=(30, 15), sticky="w")

        self.group_name_entry = ttk.Entry(self, width=20)
        self.group_name_entry.grid(row=1, column=0, padx=(200, 5), pady=(30, 15), sticky="w")

        self.set_group_btn = ttk.Button(self, text="Set", width=8, command=self.on_set_group_btn)
        self.set_group_btn.grid(row=1, column=0, padx=(335, 5), pady=(30, 15), sticky="w")

        self.cancel_group_btn = ttk.Button(self, text="Cancel", width=8, command=self.on_cancel_group_btn)
        self.cancel_group_btn.grid(row=1, column=0, padx=(400, 5), pady=(30, 15), sticky="w")

        self.prev_btn.config(state="disabled")
        self.next_btn.config(state="disabled")
        self.delete_group_btn.config(state="disabled")
        self.assign_btn.config(state="disabled")
        self.remove_btn.config(state="disabled")

    def on_set_group_btn(self):
        name = self.group_name_entry.get().strip()
        if not re.match(r"^[0-9]+$", name):
            self.err_label.config(text="Error: Encoding value must be numeric.")
            return

        if name in self.group_names:
            self.err_label.config(text="Error: Encoding value already exists.")
            return
            
        self.group_names.append(name)
        self.group_values.append([])
        self.current_group_idx = len(self.group_names) - 1

        self.set_group_label.destroy()
        self.group_name_entry.destroy()
        self.set_group_btn.destroy()
        self.cancel_group_btn.destroy()

        self.create_group_btn = ttk.Button(self, text="Create Encoding Group", command=self.on_create_group_btn)
        self.create_group_btn.grid(row=1, column=0, padx=(75, 5), pady=(30, 15), sticky="w")
        self.err_label.config(text="")

        self.update_nav()

    def on_cancel_group_btn(self):
        self.set_group_label.destroy()
        self.group_name_entry.destroy()
        self.set_group_btn.destroy()
        self.cancel_group_btn.destroy()

        self.create_group_btn = ttk.Button(self, text="Create Encoding Group", command=self.on_create_group_btn)
        self.create_group_btn.grid(row=1, column=0, padx=(75, 5), pady=(30, 15), sticky="w")
        self.err_label.config(text="")

        self.update_nav()

    def update_nav(self):
        if self.current_group_idx >= 0:
            name = self.group_names[self.current_group_idx]
            self.group_label.config(text=f"Current Encoding: {name}")
                
            self.prev_btn.config(state="normal" if self.current_group_idx > 0 else "disabled")
            self.next_btn.config(state="normal" if self.current_group_idx < len(self.group_names) - 1 else "disabled")

            self.delete_group_btn.config(state="normal")

            self.update_group_display()
        else:
            self.group_label.config(text=f"Current Encoding:")
            self.next_btn.config(state="disabled")
            self.prev_btn.config(state="disabled")
            self.delete_group_btn.config(state="disabled")

    def update_group_display(self):
        self.grouped_listbox.delete(0, tk.END)

        if self.current_group_idx >= 0:
            for value in sorted(self.group_values[self.current_group_idx]):
                self.grouped_listbox.insert(tk.END, value)

    def update_ungrouped_display(self):
        self.ungrouped_listbox.delete(0, tk.END)

        for value in sorted(self.ungrouped_values):
            self.ungrouped_listbox.insert(tk.END, value)

    def on_select_ungrouped(self):
        if self.current_group_idx >= 0:
            if len(self.ungrouped_listbox.curselection()) > 0:
                self.assign_btn.config(state="enabled")
            else:
                self.assign_btn.config(state="disabled")

    def on_select_grouped(self):
        if len(self.grouped_listbox.curselection()) > 0:
            self.remove_btn.config(state="enabled")
        else:
            self.remove_btn.config(state="disabled")

    def on_prev_btn(self):
        if self.current_group_idx > 0:
            self.current_group_idx -= 1
            self.update_nav()

    def on_next_btn(self):
        if self.current_group_idx < len(self.group_names) - 1:
            self.current_group_idx += 1
            self.update_nav()

    def on_delete_btn(self):
        if self.current_group_idx < 0:
            return

        self.ungrouped_values.update(self.group_values[self.current_group_idx])

        del self.group_values[self.current_group_idx]
        del self.group_names[self.current_group_idx]

        self.current_group_idx = max(0, self.current_group_idx - 1)

        self.update_nav()
        self.update_ungrouped_display()

    def on_assign_btn(self):
        selected_indices = list(self.ungrouped_listbox.curselection())

        if not selected_indices:
            return

        for i in selected_indices:
            value = self.ungrouped_listbox.get(i)

            if self.feat_dtype == int:
                value = int(value)
            elif self.feat_dtype == float:
                value = float(value)

            self.ungrouped_values.remove(value)
            self.group_values[self.current_group_idx].append(value)

        self.group_values[self.current_group_idx].sort()

        self.finish_btn.config(state="normal" if not self.ungrouped_values else "disabled")
        self.assign_btn.config(state="disabled")

        self.update_group_display()
        self.update_ungrouped_display()

    def on_remove_btn(self):
        selected_indices = list(self.grouped_listbox.curselection())

        if not selected_indices:
            return

        for i in selected_indices:
            value = self.grouped_listbox.get(i)

            if self.feat_dtype == int:
                value = int(value)
            elif self.feat_dtype == float:
                value = float(value)

            self.group_values[self.current_group_idx].remove(value)
            self.ungrouped_values.add(value)

        self.remove_btn.config(state="disabled")
        self.finish_btn.config(state="disabled")

        self.update_group_display()
        self.update_ungrouped_display()

    def on_finish_button(self):
        group_dict = {name: values for name, values in zip(self.group_names, self.group_values)}
        self.manager.params["groups"] = group_dict

        if self.manager.frame_count() != 2:
                self.manager.delete_frame_by_index(2)

        self.manager.add_frame(SaveCustomEncodeFrame, manager=self.manager)
        self.manager.show_frame(1)

class SaveCustomEncodeFrame(GenerateCodeFrame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.params = manager.params
        
        top_label = ttk.Label(
            self.content_frame,
            text="Select How to Save Changes",
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, columnspan=2, padx=5, pady=(20,5), sticky="n")

        save_df_text = ttk.Label(
            self.content_frame,
            text="Save Changes to:",
            font=("Arial", 12)
        )
        save_df_text.grid(row=1, column=0, padx=5, pady=(30,15), sticky="w")

        self.save_df_var = tk.StringVar(value="")

        self.current_df_radio = ttk.Radiobutton(
            self.content_frame,
            text="Current DataFrame",
            variable=self.save_df_var,
            value="current",
            command=self.on_save_df_selected
        )
        self.current_df_radio.grid(row=1, column=0, padx=(150,5), pady=(30,15), sticky="w")

        self.new_df_radio = ttk.Radiobutton(
            self.content_frame,
            text="New DataFrame:",
            variable=self.save_df_var,
            value="new",
            command=self.on_save_df_selected
        )
        self.new_df_radio.grid(row=1, column=0, padx=(275, 5), pady=(30,15), sticky="w")


        self.new_df_entry = ttk.Entry(
            self.content_frame,
            state="disabled",
            width=15
        )
        self.new_df_entry.grid(row=1, column=0, padx=(400, 5), pady=(30,15), sticky="w")

        save_col_text = ttk.Label(
        self.content_frame,
        text="Save Column:",
        font=("Arial", 12)
        )
        save_col_text.grid(row=2, column=0, padx=5, pady=(30,15), sticky="w")

        self.save_col_var = tk.StringVar(value="")
        self.current_col_radio = ttk.Radiobutton(
            self.content_frame,
            text="Current Column",
            variable=self.save_col_var,
            value="current",
            command=self.on_save_col_selected
        )
        self.current_col_radio.grid(row=2, column=0, padx=(150, 5), pady=(30,15), sticky="w")

        self.new_col_radio = ttk.Radiobutton(
            self.content_frame,
            text="New Column:",
            variable=self.save_col_var,
            value="new",
            command=self.on_save_col_selected
        )
        self.new_col_radio.grid(row=2, column=0, padx=(275, 5), pady=(30,15), sticky="w")

        self.new_col_entry = ttk.Entry(
            self.content_frame,
            state="disabled",
            width=15
        )
        self.new_col_entry.grid(row=2, column=0, padx=(400, 5), pady=(30,15), sticky="w")

        self.err_label = ttk.Label(
            self.content_frame,
            text="",
            font=("Arial", 10),
            foreground="red"
        )
        self.err_label.grid(row=3, column=0, columnspan=2, padx=5, pady=(25,5), sticky="n")

        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        self.generate_btn.config(state="disabled")
            
    def on_save_df_selected(self):
        if self.save_df_var.get() == "new":
            self.new_df_entry.config(state="normal")
        else:
            self.new_df_entry.config(state="disabled")

    def on_save_col_selected(self):
        if self.save_col_var.get() == "new":
            self.new_col_entry.config(state="normal")
        else:
            self.new_col_entry.config(state="disabled")
        self.generate_btn.config(state="normal")

    def validate_name(self, name):
        return re.match(r"^[A-Za-z]\w*$", name) is not None

    def validate_inputs(self):
        if self.save_df_var.get() == "new":
            name = self.new_df_entry.get()
            if not self.validate_name(name):
                self.err_label.config(text="Invalid DataFrame Name")
                return False
            df_names = self.winfo_toplevel().SessionData.getDFNames()
            if name in set(df_names):
                if not self.open_overwrite_popup("DataFrame", name):
                    return False
        if self.save_col_var.get() == "new":
            col = self.new_col_entry.get().strip()
            if not col:
                self.err_label.config(text="Invalid Column Name")
                return False
            if col in set(self.winfo_toplevel().SessionData.getDataFrame(self.params["df"]).columns):
                if not self.open_overwrite_popup(f"column within DataFrame {self.params["df"]}", col):
                    return False
        return True

    def open_overwrite_popup(self, item, name):
        self.popup_result = False
        dialog = PopupDialog(
            self,
            title=f"Duplicate {item}",
            message=f"A {item} named '{name}' already exists.\nDo you want to overwrite it?",
            on_right=lambda: self.set_popup_result(True),
            on_left=lambda: self.set_popup_result(False),
            rightButton="Yes",
            leftButton="No"
        )
        self.wait_window(dialog)
        return self.popup_result

    def set_popup_result(self, value):
        self.popup_result = value
        self.focus_set()

 
    def generate_code(self):
        if not self.validate_inputs():
            return

        code, imports = EncodeCustomExecutor.generate(
            df=self.params["df"],
            feature=self.params["feature"],
            groups=self.params["groups"],
            new_name=self.new_df_entry.get().strip() if self.save_df_var.get() == "new" else None,
            new_col=self.new_col_entry.get().strip() if self.save_col_var.get() == "new" else None,
            session=self.winfo_toplevel().SessionData,
            withImport=self.include_import_var.get()
        )

        if code:
            self.winfo_toplevel().SessionData.addOutput(code)
        if imports:
            self.winfo_toplevel().SessionData.addImports(imports)

        self.reset_inputs()

    def reset_inputs(self):
        self.save_df_var.set("")
        self.new_df_entry.delete(0, tk.END)
        self.new_df_entry.config(state="disabled")

        self.save_col_var.set("")
        self.new_col_entry.delete(0, tk.END)
        self.new_col_entry.config(state="disabled")

        self.err_label.config(text="")
        self.generate_btn.config(state="disabled")