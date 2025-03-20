import pandas as pd

class ImportGenerator:
    @staticmethod
    def generate(filepath, name, nrows, withImport, colab_mode=False):
        import_stmts = ["import pandas as pd"]
        code = ""
        f_op = ""

        # Determine appropriate pandas read function
        if filepath.endswith(".csv"):
            f_op = f"read_csv('{filepath}')"
        elif filepath.endswith(".tsv"):
            f_op = f"read_csv('{filepath}', sep='\\t')"
        elif filepath.endswith(".xlsx"):
            f_op = f"read_excel('{filepath}')"
        elif filepath.endswith(".txt"):
            f_op = f"read_csv('{filepath}', sep='\\t', header=None)"
        elif filepath.endswith(".json"):
            f_op = f"read_json('{filepath}')"

        # Handle Google Colab mode
        if colab_mode:
            import_stmts.append("from google.colab import files")
            f_op = f_op.replace(f"'{filepath}'", "list(uploaded.keys())[0]")
            colab_filedialog = (
                "# If using Google Colab, you must upload the dataset to Colab.\n"
                "# Running the command below will open a file prompt,\n"
                "# Click 'Choose Files' and select the dataset again.\n"
                "uploaded = files.upload()\n\n"
                "# Once uploaded, read the file into pandas using:\n"
            )
            code = colab_filedialog

        # construct file operation and head() call
        if nrows != "5":
            code += f"{name} = pd." + f_op + f"\n{name}.head({nrows})"
        else:
            code += f"{name} = pd." + f_op + f"\n{name}.head()"

        # Include import statements if requested
        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts

