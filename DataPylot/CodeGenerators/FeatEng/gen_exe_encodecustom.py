import pandas as pd

class EncodeCustomExecutor:
    @staticmethod
    def generate(df, feature, groups, new_name=None, new_col=None, session=None, withImport=False):
        import_stmts = ["import pandas as pd"]
        code = ""
        result = None

        data = session.getDataFrame(df)

        if not isinstance(data, pd.DataFrame):
            return code, import_stmts

        if new_name is None:
            new_name = df
        
        if new_col is None:
            new_col = feature

        if new_name != df:
            code += f"{new_name} = {df}.copy()\n\n"
            result = data.copy()
        else:
            result = data

        group_dict_str = "{\n"
        mapping = {}

        for encoded_value, values in groups.items():
            values_str = ", ".join(f"{repr(v)}" for v in values)
            group_dict_str += f"    {encoded_value}: [{values_str}],\n"
            for v in values:
                mapping[v] = int(encoded_value)

        group_dict_str += "}"

        code += (
            f"# Encoding categorical values into numeric groups\n"
            f"encodings = {group_dict_str}\n"
            f"mapping = {{v: k for k, vals in encodings.items() for v in vals}}\n"
            f"{new_name}['{new_col}'] = {new_name}['{feature}'].replace(mapping)\n"
        )

        result[new_col] = result[feature].replace(mapping)

        if result is not None:
            session.addDataFrame(new_name, result)

        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts
