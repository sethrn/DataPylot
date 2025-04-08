import pandas as pd

class MissingValueExecutor:
    @staticmethod
    def generate(df, feature=None, operation=None, new_name=None, new_col=None, session=None, withImport=True):
        import_stmts = ["import pandas as pd"]
        code = ""
        
        data = session.getDataFrame(df)

        if not isinstance(data, pd.DataFrame):
            return code, import_stmts

        if feature is None:
            if new_name is None:
                new_name = df

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
                    if new_name is None:
                        new_name = df

                    code += (
                        f"# Remove rows with missing values in feature '{feature}'\n"   
                        f"{new_name} = {df}.dropna(subset=['{feature}'])"
                    )
                    result = data.dropna(subset=[feature])
                case "mode":
                    if new_name is None:
                        new_name = df

                    code += (
                        f"# Impute missing values in feature '{feature}'\n"
                        f"mode_value = {df}['{feature}'].mode()[0]\n"
                        f"{new_name} = {df}.fillna({{'{feature}': mode_value}})"
                    )
                    mode_value = data[feature].mode()[0]
                    result = data.fillna({feature: mode_value})
                case "median":
                    if new_name is None:
                        new_name = df

                    code += (
                        f"# Impute missing values in feature '{feature}' with median\n"
                        f"median_value = {df}['{feature}'].median()\n"
                        f"{new_name} = {df}.fillna({{'{feature}': median_value}})"
                    )
                    median_value = data[feature].median()
                    result = data.fillna({feature: median_value})
                case "mean":
                    if new_name is None:
                        new_name = df

                    code += (
                        f"# Impute missing values in feature '{feature}' with mean\n"
                        f"mean_value = {df}['{feature}'].mean()\n"
                        f"{new_name} = {df}.fillna({{'{feature}': mean_value}})"
                    )
                    mean_value = data[feature].mean()
                    result = data.fillna({feature: mean_value})
                case "dummy":
                    code += (
                        f"# Replace feature '{feature}' to an indicator of: 1 = Value Present, 0 = Value Missing\n"
                    )
                    if new_name is None:
                        new_name = df
                    else:
                        code += f"{new_name} = {df}.copy()"

                    if new_col is None:
                        new_col = feature

                    code += (
                        f"{new_name}['{new_col}'] = {df}['{feature}'].notnull().astype(int)"
                    )
                    result = data
                    result[new_col] = data[feature].notnull().astype(int)
        
        session.addDataFrame(new_name, result)

        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts

        