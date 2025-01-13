import pandas as pd

class RenameExecutor:
    @staticmethod
    def generate(df, feature, values, rename, new_name=None, new_col=None, session=None, withImport=False):
        import_stmts = ["import pandas as pd"]
        code = ""
        result = None

        data = session.getDataFrame(df)
        if not isinstance(data, pd.DataFrame):
            return code, import_stmts
        else:
            result = data.copy()

        if not isinstance(values, list):
            return code, import_stmts

        if not new_name:
            new_name = df
        if not new_col:
            new_col = feature

        if len(values) == 1:
            single_value = values[0]
            result[new_col] = result[feature].replace(single_value, rename)

            code += (
                f"# Replace the value '{single_value}' in column '{feature}' with '{rename}'\n"
            )
            if new_name != df:
                code += f"{new_name} = {df}.copy()\n"

            code += f"{new_name}['{new_col}'] = {df}['{feature}'].replace('{single_value}', '{rename}')\n"
            
        else:
            replace_dict = {value: rename for value in values}
            result[new_col] = result[feature].replace(replace_dict)

            values_str = ", ".join([f"'{value}'" for value in values])
            code += (
                f"# Replace specified value(s) in column '{feature}' with '{rename}'\n"
                f"values = [{values_str}]\n"
                f"replace_dict = {{value: '{rename}' for value in values}}\n\n"
            )
            if new_name == df:
                code += f"{new_name}['{new_col}'] = {df}['{feature}'].replace(replace_dict)\n"
            else:
                code += f"{new_name} = {df}.copy()\n"
                code += f"{new_name}['{new_col}'] = {new_name}['{feature}'].replace(replace_dict)\n"

        if result is not None:
            session.addDataFrame(new_name, result)

        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts
