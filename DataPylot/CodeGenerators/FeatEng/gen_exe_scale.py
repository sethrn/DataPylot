import pandas as pd
from sklearn.preprocessing import StandardScaler
import numpy as np

class ScaleExecutor:
    @staticmethod
    def generate(df, features, technique, new_name=None, new_col=None, session=None, withImport=False):
        import_stmts = []
        code_lines = []
        result = None

        data = session.getDataFrame(df)

        if not isinstance(data, pd.DataFrame):
            return "", []

        if new_name is None:
            new_name = df

        result = data.copy()

        if technique == "stand":
            import_stmts.append("from sklearn.preprocessing import StandardScaler")
            code_lines.append(f"# Standardize {'multiple features' if len(features) > 1 else features[0]} using Z-score scaling")
            code_lines.append("standard_scaler = StandardScaler()")

            if new_name != df:
                code_lines.append(f"{new_name} = {df}.copy()")

            scaler = StandardScaler()

            for feat in features:
                col_name = new_col if new_col and len(features) == 1 else feat
                code_lines.append(f"{new_name}['{col_name}'] = standard_scaler.fit_transform({df}[[\"{feat}\"]])")
                result[col_name] = scaler.fit_transform(result[[feat]])

        elif technique == "log":
            import_stmts.append("import numpy as np")
            if new_name != df:
                code_lines.append(f"{new_name} = {df}.copy()")

            for feat in features:
                col_name = new_col if new_col and len(features) == 1 else feat
                code_lines.append(f"# Apply Log Transformation to '{feat}'")
                code_lines.append(f"{new_name}['{col_name}'] = np.log({df}['{feat}'] + 1)  # Add 1 to avoid log(0)")
                result[col_name] = np.log(result[feat] + 1)

        elif technique == "sqrt":
            import_stmts.append("import numpy as np")
            if new_name != df:
                code_lines.append(f"{new_name} = {df}.copy()")

            for feat in features:
                col_name = new_col if new_col and len(features) == 1 else feat
                code_lines.append(f"# Apply Square Root Transformation to '{feat}'")
                code_lines.append(f"{new_name}['{col_name}'] = np.sqrt({df}['{feat}'])")
                result[col_name] = np.sqrt(result[feat])

        session.addDataFrame(new_name, result)

        final_code = "\n".join(import_stmts) + "\n\n" + "\n".join(code_lines) if withImport else "\n".join(code_lines)

        return final_code, import_stmts
