import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

class ScaleExecutor:
    @staticmethod
    def generate(df, feature, technique, new_name=None, new_col=None, session=None, withImport=False):
        import_stmts = []
        code = ""
        result = None

        data = session.getDataFrame(df)

        if not isinstance(data, pd.DataFrame):
            return code, import_stmts

        if new_name is None:
            new_name = df
        if new_col is None:
            new_col = feature

        result = data.copy()

        if technique == "stand":
            import_stmts.append("from sklearn.preprocessing import StandardScaler")

            code += (
                f"# Standardize '{feature}' using Z-score scaling\n"
                f"standard_scaler = StandardScaler()\n"
            )
            if new_name != df:
                code += f"{new_name} = {df}.copy()\n"

            code += (
                f"{new_name}['{new_col}'] = standard_scaler.fit_transform({df}[['{feature}']])\n"
            )

            scaler = StandardScaler()
            result[new_col] = scaler.fit_transform(result[[feature]])

        elif technique == "log":
            import_stmts.append("import numpy as np")

            code += (
                f"# Apply Log Transformation to '{feature}'\n"
                f"{new_name}['{new_col}'] = np.log({df}['{feature}'] + 1)  # Adding 1 to avoid log(0)\n"
            )
            if new_name != df:
                code = f"{new_name} = {df}.copy()\n" + code

            result[new_col] = np.log(result[feature] + 1)

        elif technique == "sqrt":
            import_stmts.append("import numpy as np")

            code += (
                f"# Apply Square Root Transformation to '{feature}'\n"
                f"{new_name}['{new_col}'] = np.sqrt({df}['{feature}'])\n"
            )
            if new_name != df:
                code = f"{new_name} = {df}.copy()\n" + code

            result[new_col] = np.sqrt(result[feature])

        session.addDataFrame(new_name, result)

        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts
