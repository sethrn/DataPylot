class CorrelationGenerator:
    @staticmethod
    def generate(df, technique, withImport):
        import_stmts = [
            "import pandas as pd"
        ]

        code = ""

        match technique:
            case "Pearson Coefficient":
                method = "pearson"
                col_filter = "include='number'"
            case "Spearman Rank":
                method = "spearman"
                col_filter = "include='number'"
            case "Kendall Tau":
                method = "kendall"
                col_filter = "include='number'"

        code += (
            f"valid_cols = {df}.select_dtypes({col_filter}).columns\n"
            f"correlation_matrix = {df}[valid_cols].corr(method='{method}')\n"
            f"print(correlation_matrix)"
        )


        if withImport:
            imports_code = "\n".join(import_stmts)
            code = f"{imports_code}\n\n{code}"

        return code, import_stmts
