class StatsGenerator():
    @staticmethod
    def generate(df, shape_var, info_var, summary_var, vc_var, withImport):
        code = ""

        if shape_var:
            code += (
                f"print('Displaying Shape:')\n"
                f"print(f\"{{{df}.shape}}\\n\")\n\n"
            )
        if info_var:
            code += (
                f"print('Displaying Feature Information:')\n"
                f"print(f\"{{{df}.info()}}\\n\")\n\n"
            )
        if summary_var:
            code += (
                f"print('Displaying Summary Statistics:')\n"
                f"print(f\"{{{df}.describe()}}\\n\")\n\n"
            )
        if vc_var:
            code += (
                f"print('Displaying Value Counts:')\n"
                f"for column in {df}.columns:\n"
                f"\tprint(f\"Unique values and counts for '{{column}}':\")\n"
                f"\tprint({df}[column].value_counts())\n"
                f"\tprint(f\"Total Unique Values: {{{df}[column].nunique()}}\")\n"
                f"\tprint('=' * 50)"
            )

        import_stmt = "import pandas as pd"

        if withImport:
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmt
