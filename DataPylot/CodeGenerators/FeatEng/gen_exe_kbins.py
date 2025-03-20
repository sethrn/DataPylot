import pandas as pd
from sklearn.preprocessing import KBinsDiscretizer

class KBinsExecutor:
    @staticmethod
    def generate(df, feature, technique, encoding, nbins, new_name=None, new_col=None, prefix=None, session=None, withImport=False):
        import_stmts = ["from sklearn.preprocessing import KBinsDiscretizer"]
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

        if prefix is None:
            prefix = feature

        encode_param = "ordinal" if encoding == "ordinal" else "onehot-dense"
        strategy_param = "uniform" if technique == "distance" else "quantile"

        code += f"# Apply KBinsDiscretizer ({technique} binning with {nbins} bins)\n"
        code += f"kbins = KBinsDiscretizer(n_bins={nbins}, encode='{encode_param}', strategy='{strategy_param}')\n"
        
        kbins = KBinsDiscretizer(n_bins=nbins, encode=encode_param, strategy=strategy_param)
        transformed = kbins.fit_transform(result[[feature]])

        if encoding == "ordinal":
            code += f"{new_name}['{new_col}'] = kbins.fit_transform({new_name}[['{feature}']]).ravel()\n"
            transformed = kbins.fit_transform(result[[feature]]).ravel()
            result[new_col] = transformed

        elif encoding == "onehot":
            code += f"{new_name}_binned = kbins.fit_transform({new_name}[['{feature}']])\n"
            code += f"bin_columns = [f'{prefix}_' + str(i) for i in range({nbins})]\n"
            code += f"encoded_df = pd.DataFrame({new_name}_binned, columns=bin_columns)\n"
            code += f"{new_name} = pd.concat([{new_name}.drop(columns=['{feature}']), encoded_df], axis=1)\n"

            transformed = kbins.fit_transform(result[[feature]])
            onehot_df = pd.DataFrame(transformed, columns=[f"{prefix}_{i}" for i in range(nbins)])
            result = pd.concat([result.drop(columns=[feature]), onehot_df], axis=1)

        session.addDataFrame(new_name, result)

        if result is not None:
            session.addDataFrame(new_name, result)

        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts
