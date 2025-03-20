import tkinter as tk
from tkinter import ttk
import re

from CodeGenerators.FeatEng.gen_exe_binrange import BinRangeExecutor
from components.Patterns.generate_frame import GenerateCodeFrame
from components.Patterns.popup_dialog import PopupDialog

class BinRangeFrame(ttk.Frame):
    def __init__(self, parent, manager):
        super().__init__(parent)

        self.manager = manager
        self.df_name = self.manager.params["df"]
        self.feature = self.manager.params["feature"]

        self.bin_names = []
        self.lower_bounds = []
        self.upper_bounds = []
        self.current_group_idx = -1

        self.string_label = False

        df = self.winfo_toplevel().SessionData.getDataFrame(self.df_name)
        if df is not None:
            self.lower_bound = float(min(df[self.feature].dropna()))
            self.upper_bound = float(max(df[self.feature].dropna()))

        top_label = ttk.Label(
            self, text="Customize Bins by Specifying Labels and Ranges",
            font=("Arial", 14)
        )
        top_label.grid(row=0, column=0, padx=5, pady=(20, 5), sticky="n")

        self.current_bin_label = ttk.Label(self, text="Current Bin:", font=("Arial", 12))
        self.current_bin_label.grid(row=1, column=0, padx=(150, 5), pady=(45, 5), sticky="w")

        self.bin_name_entry = ttk.Entry(self, width=20, state="readonly")
        self.bin_name_entry.grid(row=1, column=0, padx=(265, 5), pady=(45, 5), sticky="w")

        self.lower_range_label = ttk.Label(self, text="Lower Bound:", font=("Arial", 12))
        self.lower_range_label.grid(row=2, column=0, padx=(150, 5), pady=(15, 5), sticky="w")

        self.lower_bound_entry = ttk.Entry(self, width=20, state="readonly")
        self.lower_bound_entry.grid(row=2, column=0, padx=(265, 5), pady=(15, 5), sticky="w")

        self.upper_range_label = ttk.Label(self, text="Upper Bound:", font=("Arial", 12))
        self.upper_range_label.grid(row=3, column=0, padx=(150, 5), pady=(15, 5), sticky="w")

        self.upper_bound_entry = ttk.Entry(self, width=20, state="readonly")
        self.upper_bound_entry.grid(row=3, column=0, padx=(265, 5), pady=(15, 5), sticky="w")

        self.prev_btn = ttk.Button(self, text="Previous Bin", width=14, state="disabled", command=self.on_prev_btn)
        self.prev_btn.grid(row=4, column=0, padx=(150, 5), pady=(15, 5), sticky="w")

        self.next_btn = ttk.Button(self, text="Next Bin", width=14, state="disabled", command=self.on_next_btn)
        self.next_btn.grid(row=4, column=0, padx=(250, 5), pady=(15, 5), sticky="w")

        self.create_group_btn = ttk.Button(self, text="Create Bin", width=14, command=self.on_create_group_btn)
        self.create_group_btn.grid(row=1, column=0, padx=(450, 5), pady=(45, 5), sticky="w")

        self.edit_group_btn = ttk.Button(self, text="Edit Bin", width=14, state="disabled", command=self.on_edit_group_btn)
        self.edit_group_btn.grid(row=2, column=0, padx=(450, 5), pady=(15, 5), sticky="w")

        self.delete_group_btn = ttk.Button(self, text="Delete Bin", width=14, state="disabled", command=self.on_delete_group_btn)
        self.delete_group_btn.grid(row=4, column=0, padx=(450, 5), pady=(15, 5), sticky="w")

        self.finish_btn = ttk.Button(self, text="Finish", width=20, state="disabled", command=self.on_finish_btn)
        self.finish_btn.grid(row=5, column=0, padx=5, pady=(50, 5), sticky="n")

        self.err_label = ttk.Label(self, text="", font=("Arial", 10), foreground="red")
        self.err_label.grid(row=6, column=0, padx=5, pady=(5, 10), sticky="n")

        self.grid_columnconfigure(0, weight=1)

    def on_create_group_btn(self):
        self.err_label.config(text="")
        self.bin_name_entry.config(state="normal")
        self.bin_name_entry.delete(0, tk.END)
        self.lower_bound_entry.config(state="normal")
        self.lower_bound_entry.delete(0, tk.END)
        self.upper_bound_entry.config(state="normal")
        self.upper_bound_entry.delete(0, tk.END)

        self.prev_btn.config(state="disabled")
        self.next_btn.config(state="disabled")
        self.delete_group_btn.config(state="disabled")

        self.create_group_btn.config(
            text="Save New Bin",
            command=self.on_save_group_btn
        )

        self.edit_group_btn.config(
            text="Cancel",
            command=self.on_cancel_btn
        )

    def on_save_group_btn(self):
        name = self.bin_name_entry.get().strip()

        if not self.validate_bin_inputs():
            return

        if not self.string_label:
            name = int(name)

        lower = float(self.lower_bound_entry.get().strip())
        upper = float(self.upper_bound_entry.get().strip())

        self.bin_names.append(name)
        self.lower_bounds.append(lower)
        self.upper_bounds.append(upper)
        self.current_group_idx = len(self.bin_names) - 1

        self.create_group_btn.config(text="Create Bin", command=self.on_create_group_btn)
        self.edit_group_btn.config(text="Edit Bin", command=self.on_edit_group_btn)

        self.update_nav()


    def on_edit_group_btn(self):
        self.err_label.config(text="")
        if self.current_group_idx == -1:
            return

        self.bin_name_entry.config(state="normal")
        self.lower_bound_entry.config(state="normal")
        self.upper_bound_entry.config(state="normal")
        self.prev_btn.config(state="disabled")
        self.next_btn.config(state="disabled")
        self.delete_group_btn.config(state="disabled")

        self.create_group_btn.config(
            text="Save Edits",
            command=self.on_save_edit_btn
        )

        self.edit_group_btn.config(
            text="Cancel",
            command=self.on_cancel_btn
        )

    def on_save_edit_btn(self):
        name = self.bin_name_entry.get().strip()
        lower = self.lower_bound_entry.get().strip()
        upper = self.upper_bound_entry.get().strip()

        bin_names = self.bin_names[:]
        bin_names.pop(self.current_group_idx)
        lower_bounds = self.lower_bounds[:]
        lower_bounds.pop(self.current_group_idx)
        upper_bounds = self.upper_bounds[:]
        upper_bounds.pop(self.current_group_idx)

        if not self.validate_bin_inputs(bin_names, lower_bounds, upper_bounds):
            return
        if not self.string_label:
            name = int(self.bin_name_entry.get().strip())

        self.bin_names[self.current_group_idx] = name
        self.lower_bounds[self.current_group_idx] = float(lower)
        self.upper_bounds[self.current_group_idx] = float(upper)

        self.create_group_btn.config(
            text="Create Bin",
            command=self.on_create_group_btn
        )
        self.edit_group_btn.config(
            text="Edit Bin",
            command=self.on_edit_group_btn
        )

        self.update_nav()


    def on_cancel_btn(self):
        self.create_group_btn.config(
            text="Create Bin",
            command=self.on_create_group_btn
        )
        self.edit_group_btn.config(
            text="Edit Bin",
            command=self.on_edit_group_btn
        )

        self.update_nav()

    def validate_bin_inputs(self, bin_names=None, lower_bounds=None, upper_bounds=None):
        if bin_names is None:
            bin_names = self.bin_names
        if lower_bounds is None:
            lower_bounds = self.lower_bounds
        if upper_bounds is None:
            upper_bounds = self.upper_bounds

        name = self.bin_name_entry.get().strip()
        lower = self.lower_bound_entry.get().strip()
        upper = self.upper_bound_entry.get().strip()

        if not name:
            self.err_label.config(text="Error: Bin label cannot be empty.")
            return False

        try:
            name = int(name)
        except ValueError:
            self.string_label = True

        if name in bin_names:
            self.err_label.config(text="Error: Bin Name already exists.")
            return False
        else:
            self.err_label.config(text="Warning: Non-integer bin label detected, this column won't be numeric.")

        try:
            lower = float(lower)
            upper = float(upper)
        except ValueError:
            self.err_label.config(text="Error: Lower and Upper bounds must be numeric.")
            return False

        if lower >= upper:
            self.err_label.config(text="Error: Lower bound must be less than upper bound.")
            return False

        # Check for overlapping bins
        for i in range(len(lower_bounds)):
            existing_lower = lower_bounds[i]
            existing_upper = upper_bounds[i]
            if not (upper <= existing_lower or lower >= existing_upper):
                self.err_label.config(text=f"Error: Overlaps with bin '{bin_names[i]}'.")
                return False

        return True

    def on_delete_group_btn(self):
        if self.current_group_idx < 0:
            return

        self.err_label.config(text="")
        del self.bin_names[self.current_group_idx]
        del self.lower_bounds[self.current_group_idx]
        del self.upper_bounds[self.current_group_idx]

        self.current_group_idx = max(0, self.current_group_idx - 1)

        self.update_nav()


    def on_prev_btn(self):
        if self.current_group_idx > 0:
            self.current_group_idx -= 1
            self.update_nav()

    def on_next_btn(self):
        if self.current_group_idx < len(self.bin_names) - 1:
            self.err_label.config(text="")
            self.current_group_idx += 1
            self.update_nav()


    def update_nav(self):
        self.string_label = False
        if not self.bin_names:
            self.current_group_idx = -1
            self.bin_name_entry.delete(0, tk.END)
            self.lower_bound_entry.delete(0, tk.END)
            self.upper_bound_entry.delete(0, tk.END)
            self.bin_name_entry.config(state="readonly")
            self.lower_bound_entry.config(state="readonly")
            self.upper_bound_entry.config(state="readonly")
            self.prev_btn.config(state="disabled")
            self.next_btn.config(state="disabled")
            self.edit_group_btn.config(state="disabled")
            self.delete_group_btn.config(state="disabled")
            self.finish_btn.config(state="disabled")
            return

        # Ensure current index is within range
        self.current_group_idx = max(0, min(self.current_group_idx, len(self.bin_names) - 1))

        # Update UI fields with current bin info
        bin_name = self.bin_names[self.current_group_idx]
        lower = self.lower_bounds[self.current_group_idx]
        upper = self.upper_bounds[self.current_group_idx]

        self.bin_name_entry.config(state="normal")
        self.bin_name_entry.delete(0, tk.END)
        self.bin_name_entry.insert(0, bin_name)
        self.bin_name_entry.config(state="readonly")

        self.lower_bound_entry.config(state="normal")
        self.lower_bound_entry.delete(0, tk.END)
        self.lower_bound_entry.insert(0, str(lower))
        self.lower_bound_entry.config(state="readonly")

        self.upper_bound_entry.config(state="normal")
        self.upper_bound_entry.delete(0, tk.END)
        self.upper_bound_entry.insert(0, str(upper))
        self.upper_bound_entry.config(state="readonly")

        # Enable/disable buttons based on navigation index
        self.prev_btn.config(state="normal" if self.current_group_idx > 0 else "disabled")
        self.next_btn.config(state="normal" if self.current_group_idx < len(self.bin_names) - 1 else "disabled")
       
        self.edit_group_btn.config(state="normal")
        self.delete_group_btn.config(state="normal")
        self.finish_btn.config(state="normal")

    def on_finish_btn(self):
        group_dict = {name: [lower, upper] for name, lower, upper in zip(self.bin_names, self.lower_bounds, self.upper_bounds)}
        self.manager.params["bins"] = group_dict

        if self.manager.frame_count() != 2:
            self.manager.delete_frame_by_index(2)

        self.manager.add_frame(SaveBinRangeFrame, manager=self.manager)
        self.manager.show_frame(1)

class SaveBinRangeFrame(GenerateCodeFrame):
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

        code, imports = BinRangeExecutor.generate(
            df=self.params["df"],
            feature=self.params["feature"],
            groups=self.params["bins"],
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
