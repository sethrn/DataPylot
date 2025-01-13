import pandas as pd

class RemoveExecutor:
    @staticmethod
    def generate(df, features, new_name=None, session=None, withImport=False):
        import_stmts = ["import pandas as pd"]
        code = ""

        data = session.getDataFrame(df)
        if not isinstance(data, pd.DataFrame):
            return code, import_stmts
        else:
            result = data.copy()

        if not new_name:
            new_name = df

        if not isinstance(features, list) or not features:
            return code, import_stmts

        features_str = ", ".join([f"'{feature}'" for feature in features])
        code += f"# Remove specified features from DataFrame '{df}'\n"
        if new_name != df:
            code += f"{new_name} = {df}.copy()\n"
        
        code += f"{new_name}.drop(columns=[{features_str}], inplace=True, errors='ignore')\n"

        result = data.drop(columns=features, inplace=False)

        if result is not None:
            session.addDataFrame(new_name, result)

        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts
