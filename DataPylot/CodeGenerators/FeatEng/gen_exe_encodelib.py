import pandas as pd
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
import category_encoders as ce

class EncodeLibExecutor:
    @staticmethod
    def generate(df, feature, technique, new_name, new_col, ordinal_order, drop_first, prefix, session=None, withImport=False):
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

        if new_name != df:
            code += f"{new_name} = {df}.copy()\n"
            result = data.copy()
        else:
            result = data

        if technique == "ordinal":
            import_stmts.append("from sklearn.preprocessing import OrdinalEncoder")

            if ordinal_order is None or not isinstance(ordinal_order, list):
                return code, import_stmts
            
            code += f"# Ordinal Encoding: Assigning integer ranks based on defined order\n"
            code += f"ordinal_encoder = OrdinalEncoder(categories=[{ordinal_order}])\n"
            code += f"{new_name}['{new_col}'] = ordinal_encoder.fit_transform({new_name}[['{feature}']])\n"

            result[new_col] = OrdinalEncoder(categories=[ordinal_order]).fit_transform(result[[feature]])

        elif technique == "onehot":
            import_stmts.append("import pandas as pd")

            drop_first_str = ", drop_first=True" if drop_first == "yes" else ""

            code += f"# One-Hot Encoding: Creating separate binary columns per category\n"
            code += f"{new_name} = pd.get_dummies({new_name}, columns=['{feature}'], dtype=int, prefix='{prefix}'{drop_first_str})\n"

            result = pd.get_dummies(result, columns=[feature], dtype=int, prefix=prefix, drop_first=drop_first)

        elif technique == "binary":
            import_stmts.append("import category_encoders as ce")

            code += f"# Binary Encoding: Converting categorical values into binary representation\n"
            code += f"binary_encoder = ce.BinaryEncoder(cols=['{feature}'])\n"
            code += f"encoded_df = binary_encoder.fit_transform({new_name}[['{feature}']])\n"
            code += f"{new_name} = pd.concat([{new_name}.drop(columns=['{feature}']), encoded_df], axis=1)\n"

            encoder = ce.BinaryEncoder(cols=[feature])
            encoded_df = encoder.fit_transform(result[[feature]])
            result = pd.concat([result.drop(columns=[feature]), encoded_df], axis=1)

        if result is not None:
            session.addDataFrame(new_name, result)

        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts
