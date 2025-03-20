import pandas as pd

class InteractionExecutor:
    @staticmethod
    def generate(df, feature1, feature2, new_col, new_name=None, session=None, withImport=False):
        import_stmts = []
        code = ""
        result = None

        data = session.getDataFrame(df)

        if not isinstance(data, pd.DataFrame):
            return code, import_stmts

        if new_name is None:
            new_name = df 

        if new_name != df:
            code += f"{new_name} = {df}.copy()\n"
            result = data.copy()
        else:
            result = data

        code += f"# Creating interaction term: {new_col} = {feature1} * {feature2}\n"
        code += f"{new_name}['{new_col}'] = {new_name}['{feature1}'] * {new_name}['{feature2}']\n"


        result[new_col] = result[feature1] * result[feature2]

        session.addDataFrame(new_name, result)

        return code, import_stmts
