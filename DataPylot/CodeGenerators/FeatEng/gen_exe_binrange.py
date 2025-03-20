import pandas as pd

class BinRangeExecutor:
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

        # Construct bin mapping dictionary
        bin_mapping = {}
        group_dict_str = "{\n"
        
        for name, (lower, upper) in groups.items():
            bin_mapping[(lower, upper)] = name
            group_dict_str += f"    ({lower}, {upper}): {repr(name)},\n"

        group_dict_str += "}"
        
        # Generate code for binning logic
        code += f"# Define bin mapping\nbin_mapping = {group_dict_str}\n\n"

        code += f"# Apply bin mapping using a function\n"
        code += f"def map_bins(value):\n"
        code += f"    for (lower, upper), name in bin_mapping.items():\n"
        code += f"        if lower <= value < upper:\n"
        code += f"            return name\n"
        code += f"    return None  # Should not happen if bins are properly defined\n\n"
        
        code += f"{new_name}['{new_col}'] = {new_name}['{feature}'].map(map_bins)\n"

        # Execute the transformation
        def map_bins(value):
            for (lower, upper), name in bin_mapping.items():
                if lower <= value < upper:
                    return name
            return None

        result[new_col] = result[feature].map(map_bins)

        # Add modified DataFrame to session
        if result is not None:
            session.addDataFrame(new_name, result)

        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts
