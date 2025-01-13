class ImportGenerator():
    @staticmethod
    def generate(filepath, name, nrows, withImport):
        f_op = ""
        if filepath.endswith(".csv"):
            f_op = f"read_csv('{filepath}')"
        elif filepath.endswith(".tsv"):
            f_op = f"read_csv('{filepath}', sep='\t')"
        elif filepath.endswith(".xlsx"):
            f_op = f"read_excel('{filepath}')"
        elif filepath.endswith(".txt"):
            f_op = f"read_csv('{filepath}', sep='\t', header=None)"
        elif filepath.endswith(".json"):
            f_op = f"read_json('{filepath}')"

        if nrows != "5":
            code = f"{name} = pd." + f_op + f"\n{name}.head({nrows})"
        else:
            code = f"{name} = pd." + f_op + f"\n{name}.head()"

        import_stmt = "import pandas as pd"

        if withImport:
            code = f"{import_stmt}\n\n" + code

        return code, import_stmt


