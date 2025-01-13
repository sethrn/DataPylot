import pandas as pd

class MissingValueExecutor:
    @staticmethod
    def generate(df, feature=None, operation=None, new_name=None, session=None, withImport=True):
        import_stmts = ["import pandas as pd"]
        code = ""
        
        data = session.getDataFrame(df)

        if not isinstance(data, pd.DataFrame):
            return code, import_stmts

        if new_name is None:
            new_name = df

        if feature is None:
            code += (
                f"# Remove rows with missing values from the entire dataset\n"
                f"{new_name} = {df}.dropna()"
            )
            result = data.dropna()
        else:
            if feature not in data.columns:
                return code, import_stmts
            match operation:
                case "remove":
                    code += (
                        f"# Remove rows with missing values in feature '{feature}'\n"   
                        f"{new_name} = {df}.dropna(subset=['{feature}'])"
                    )
                    result = data.dropna(subset=[feature])
                case "mode":
                    code += (
                        f"# Impute missing values in feature '{feature}'\n"
                        f"mode_value = {df}['{feature}'].mode()[0]\n"
                        f"{new_name} = {df}.fillna({{'{feature}': mode_value}})"
                    )
                    mode_value = data[feature].mode()[0]
                    result = data.fillna({feature: mode_value})
                case "median":
                    code += (
                        f"# Impute missing values in feature '{feature}' with median\n"
                        f"median_value = {df}['{feature}'].median()\n"
                        f"{new_name} = {df}.fillna({{'{feature}': median_value}})"
                    )
                    median_value = data[feature].median()
                    result = data.fillna({feature: median_value})
                case "mean":
                    code += (
                        f"# Impute missing values in feature '{feature}' with mean\n"
                        f"mean_value = {df}['{feature}'].mean()\n"
                        f"{new_name} = {df}.fillna({{'{feature}': mean_value}})"
                    )
                    mean_value = data[feature].mean()
                    result = data.fillna({feature: mean_value})

        session.addDataFrame(new_name, result)

        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts

        