import pandas as pd

class BinCustomExecutor:
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
            code += f"{new_name} = {df}.copy()\n"
            result = data.copy()
        else:
            result = data

        group_dict_str = "{\n"
        for name, values in groups.items():
            formatted_values = ", ".join(f"'{v}'" if isinstance(v, str) else str(v) for v in values)
            group_dict_str += f"    {repr(name)}: [{formatted_values}],\n"
        group_dict_str += "}"

        code += f"""
            # Define custom bin mapping
            custom_bin_mapping = {group_dict_str}

            # Function to map values to user-defined bins
            def map_bins(value):
                for bin_name, bin_values in custom_bin_mapping.items():
                    if value in bin_values:
                        return bin_name
                return None  # Handle unmapped values gracefully

            # Apply mapping function to feature column
            {new_name}["{new_col}"] = {new_name}["{feature}"].map(map_bins)
            """

        def map_bins(value):
            for bin_name, bin_values in groups.items():
                if value in bin_values:
                    return bin_name
            return None

        result[new_col] = result[feature].map(map_bins)

        if result is not None:
            session.addDataFrame(new_name, result)
        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts
