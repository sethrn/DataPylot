class OutlierGenerator:
    @staticmethod
    def generate(df, technique, param, withImport):
        import_stmts = [
            "import pandas as pd"
        ]
        code = ""

        match technique:
            case "Tukey":
                code += (
                    f"# Detecting outliers using Tukey's Fence with multiplier {param}\n"
                    f"numeric_cols = {df}.select_dtypes(include='number').columns\n"
                    f"for col in numeric_cols:\n"
                    f"    Q1 = {df}[col].quantile(0.25)\n"
                    f"    Q3 = {df}[col].quantile(0.75)\n"
                    f"    IQR = Q3 - Q1\n"
                    f"    lower_bound = Q1 - ({param} * IQR)\n"
                    f"    upper_bound = Q3 + ({param} * IQR)\n"
                    f"\n"
                    f"    outliers_below = {df}[{df}[col] < lower_bound]\n"
                    f"    outliers_above = {df}[{df}[col] > upper_bound]\n"
                    f"    total_outliers = len(outliers_below) + len(outliers_above)\n"
                    f"\n"
                    f"    print(f\"Feature: {{col}}\")\n"
                    f"    print(f\"Lower Bound: {{lower_bound:.3f}}, Median: {{{df}[col].quantile(.5):.3f}}, Upper Bound: {{upper_bound:.3f}}\")\n"
                    f"    print(f\"Outliers Below: {{len(outliers_below)}}\")\n"
                    f"    print(f\"Outliers Above: {{len(outliers_above)}}\")\n"
                    f"    print(f\"Total Outliers: {{total_outliers}}\")\n"
                    f"    print('=' * 50)"
                )
            case "ZScore":
                code += (
                    f"# Detecting outliers using Z-Score with threshold {param}\n"
                    f"numeric_cols = {df}.select_dtypes(include='number').columns\n"
                    f"outlier_summary = []\n"
                    f"for col in numeric_cols:\n"
                    f"    mean = {df}[col].mean()\n"
                    f"    std = {df}[col].std()\n"
                    f"    lower_bound = mean - ({param} * std)\n"
                    f"    upper_bound = mean + ({param} * std)\n"
                    f"\n"
                    f"    outliers_below = {df}[{df}[col] < lower_bound]\n"
                    f"    outliers_above = {df}[{df}[col] > upper_bound]\n"
                    f"    total_outliers = len(outliers_below) + len(outliers_above)\n"
                    f"\n"
                    f"    print(f\"Feature: {{col}}\")\n"
                    f"    print(f\"Lower Bound: {{lower_bound:.3f}}, Median: {{{df}[col].quantile(.5):.3f}}, Upper Bound: {{upper_bound:.3f}}\")\n"
                    f"    print(f\"Outliers Below: {{len(outliers_below)}}\")\n"
                    f"    print(f\"Outliers Above: {{len(outliers_above)}}\")\n"
                    f"    print(f\"Total Outliers: {{total_outliers}}\")\n"
                    f"    print('=' * 50)"
                )
            case "":
                code += (
                    f"# Detecting rare categories with threshold {param:.2%}\n"
                    f"categorical_cols = {df}.select_dtypes(include=['object', 'category']).columns\n"
                    f"for col in categorical_cols:\n"
                    f"    unique_vals = {df}[col].nunique()\n"
                    f"    if unique_vals == len({df}):\n"
                    f"        continue  # Skip unique identifier columns\n"
                    f"    value_counts = {df}[col].value_counts()\n"
                    f"    rare_categories = value_counts[value_counts < (0.01)*len({df})]\n"
                    f"    if not rare_categories.empty:\n"
                    f"        print(f\"Column: {{rare_categories}}\")\n"
                    f"        print('=' * 50)"
                )

        if withImport:
            imports_code = "\n".join(import_stmts)
            code = f"{imports_code}\n\n{code}"

        return code, import_stmts


class MissingValGenerator:
    @staticmethod
    def generate(df, withImport):
        import_stmts = [
            "import pandas as pd"
        ]
        code = (
            f"# Detecting missing values in the DataFrame\n"
            f"missing_counts = {df}.isnull().sum()\n"
            f"print(\"Identifying missing values\\n\")\n"
            f"for col, count in missing_counts.items():\n"
            f"    if count > 0:\n"
            f"        print(f\"Feature: {{col}}, Missing Count: {{count}}\")\n"
        )

        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts
