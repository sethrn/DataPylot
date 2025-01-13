from numpy._core.defchararray import upper
import pandas as pd

class OutlierExecutor:
    @staticmethod
    def generate(df, operation, feature, bound, technique, param, param2=None, new_name=None, new_col=None, session=None, withImport=False):
        import_stmts = ["import pandas as pd"]
        code = ""
        result = None

        data = session.getDataFrame(df)

        if not isinstance(data, pd.DataFrame):
            return code, import_stmts

        try:
            param = float(param)
            if param2:
                param2 = float(param2)
        except (ValueError):
            return code, import_stmts
        
        if feature is None:
            if new_name is None:
                new_name = df

            code += (
                f"numeric_cols = {df}.select_dtypes(include='number').columns\n"
                f"for col in numeric_cols:\n"
            )
            numeric_cols = data.select_dtypes(include='number').columns
            if technique == "tukey":
                code += (
                    f"    Q1 = {df}[col].quantile(0.25)\n"
                    f"    Q3 = {df}[col].quantile(0.75)\n"
                    f"    IQR = Q3 - Q1"
                    f"\n"
                )
                if bound in ["lower", "both"]:
                    code += (
                        f"    lower_bound = Q1 - {param} * IQR\n"
                        f"    {new_name} = {df}[{df}[col] >= lower_bound]\n"
                    )
                        
                if bound in ["upper", "both"]:
                    code += (
                        f"    upper_bound = Q3 + {param} * IQR\n"
                        f"    {new_name} = {df}[{df}[col] <= upper_bound]"
                    )
                       
                for col in numeric_cols:
                    Q1 = data[col].quantile(0.25)
                    Q3 = data[col].quantile(0.75)
                    IQR = Q3 - Q1

                    if bound in ["lower", "both"]:
                        lower_bound = Q1 - param * IQR
                        result = data[data[col] >= lower_bound]
                    if bound in ["upper", "both"]:
                        upper_bound = Q3 + param * IQR
                        result = data[data[col] <= upper_bound]

            elif technique == "zscore":
                code += (
                    f"    mean = {df}[col].mean()\n"
                    f"    std = {df}[col].std()\n"
                    f"\n"
                )
                if bound in ["lower", "both"]:
                    code += (
                        f"    lower_bound = mean - {param} * std\n"
                        f"    {new_name} = {df}[{df}[col] >= lower_bound]\n"
                    )
                if bound in ["upper", "both"]:
                    code += (
                        f"    upper_bound = mean + {param} * std\n"
                        f"    {new_name} = {df}[{df}[col] <= upper_bound]"
                    )
                    
                for col in numeric_cols:
                    mean = data[col].mean()
                    std = data[col].std()
                    if bound in ["lower", "both"]:
                        lower_bound = mean - param * std
                        result = data[data[col] >= lower_bound]
                    if bound in ["upper", "both"]:
                        upper_bound = mean + param * std
                        result = data[data[col] <= upper_bound]
 
        else:
            result = data.copy()
            if technique == "tukey":
                code += (
                    f"Q1 = {df}['{feature}'].quantile(0.25)\n"
                    f"Q3 = {df}['{feature}'].quantile(0.75)\n"
                    f"IQR = Q3 - Q1\n"
                    f"\n"
                )
                Q1 = data[feature].quantile(0.25)
                Q3 = data[feature].quantile(0.75)
                IQR = Q3 - Q1

                if bound in ["lower", "both"]:
                    code += f"lower_bound = Q1 - {param} * IQR\n"
                    lower_bound = Q1 - {param} * IQR
                        
                    if operation == "remove":
                        if new_name is None:
                            new_name = df
                        code += (
                            f"{new_name} = {df}[{df}['{feature}'] >= lower_bound]\n"
                        )
                        result = data[data[feature] >= lower_bound]
                    elif operation == "cap":
                        if new_name is None:
                            new_name = df                           
                        elif new_name != df:
                            code += f"{new_name} = {df}.copy()\n"

                        if new_col is None:
                            new_col = feature

                        code += (
                            f"{new_name}['{new_col}'] = {df}['{feature}'].apply(lambda x: max(x, lower_bound))\n"
                        )
                        result[new_col] = data[feature].apply(lambda x: max(x, lower_bound))
                if bound in ["upper", "both"]:
                    code += f"upper_bound = Q3 + {param} * IQR\n"
                    upper_bound = Q3 + param * IQR
                    if operation == "remove":
                        if new_name is None:
                            new_name = df
                        code += (
                            f"{new_name} = {df}[{df}['{feature}'] <= upper_bound]\n"
                        )
                        result = data[data[feature] <= upper_bound]
                    elif operation == "cap":
                        if new_name is None:
                            new_name = df                           
                        elif bound != "both" and new_name != df:
                            code += f"{new_name} = {df}.copy()\n"

                        if new_col is None:
                            new_col = feature

                        code += (
                            f"{new_name}['{new_col}'] = {df}['{feature}'].apply(lambda x: min(x, upper_bound))\n"
                        )
                        result[new_col] = data[feature].apply(lambda x: min(x, upper_bound))
            elif technique == "zscore":
                code += (
                    f"mean = {df}['{feature}'].mean()\n"
                    f"std = {df}['{feature}'].std()\n"
                    f"\n"
                )
                mean = data[feature].mean()
                std = data[feature].std()

                if bound in ["lower", "both"]:
                    code += f"lower_bound = mean - {param} * std\n"
                    lower_bound = mean - param * std
                        
                    if operation == "remove":
                        if new_name is None:
                            new_name = df
                        code += (
                            f"{new_name} = {df}[{df}['{feature}'] >= lower_bound]\n"
                        )
                        result = data[data[feature] >= lower_bound]
                    elif operation == "cap":
                        if new_name is None:
                            new_name = df                           
                        elif new_name != df:
                            code += f"{new_name} = {df}.copy()\n"

                        if new_col is None:
                            new_col = feature

                        code += (
                            f"{new_name}['{new_col}'] = {df}['{feature}'].apply(lambda x: max(x, lower_bound))\n"
                        )
                        result[new_col] = data[feature].apply(lambda x: max(x, lower_bound))
                if bound in ["upper", "both"]:
                    code += f"upper_bound =mean + {param} * std\n"
                    upper_bound = mean + param * std
                    if operation == "remove":
                        if new_name is None:
                            new_name = df
                        code += (
                            f"{new_name} = {df}[{df}['{feature}'] <= upper_bound]\n"
                        )
                        result = data[data[feature] <= upper_bound]
                    elif operation == "cap":
                        if new_name is None:
                            new_name = df                           
                        elif bound != "both" and new_name != df:
                            code += f"{new_name} = {df}.copy()\n"

                        if new_col is None:
                            new_col = feature

                        code += (
                            f"{new_name}['{new_col}'] = {df}['{feature}'].apply(lambda x: min(x, upper_bound))\n"
                        )
                        result[new_col] = data[feature].apply(lambda x: min(x, upper_bound))
            elif technique == "custom":
                if bound in ["lower", "both"]:
                    code += f"lower_bound = {param}\n"
                    lower_bound = param
                        
                    if operation == "remove":
                        if new_name is None:
                            new_name = df
                        code += (
                            f"{new_name} = {df}[{df}['{feature}'] >= lower_bound]\n"
                        )
                        result = data[data[feature] >= lower_bound]
                    elif operation == "cap":
                        if new_name is None:
                            new_name = df                           
                        elif new_name != df:
                            code += f"{new_name} = {df}.copy()\n"

                        if new_col is None:
                            new_col = feature

                        code += (
                            f"{new_name}['{new_col}'] = {df}['{feature}'].apply(lambda x: max(x, lower_bound))\n"
                        )
                        result[new_col] = data[feature].apply(lambda x: max(x, lower_bound))
                if bound in ["upper", "both"]:
                    if bound == "upper":
                        code += f"upper_bound = {param}\n"
                        upper_bound = param
                    else:
                        code += f"upper_bound = {param2}\n"
                        upper_bound = param2
                    
                    if operation == "remove":
                        if new_name is None:
                            new_name = df
                        code += (
                            f"{new_name} = {df}[{df}['{feature}'] <= upper_bound]\n"
                        )
                        result = data[data[feature] <= upper_bound]
                    elif operation == "cap":
                        if new_name is None:
                            new_name = df                           
                        elif bound != "both" and new_name != df:
                            code += f"{new_name} = {df}.copy()\n"

                        if not new_col:
                            new_col = feature

                        code += (
                            f"{new_name}['{new_col}'] = {df}['{feature}'].apply(lambda x: min(x, upper_bound))\n"
                        )
                        result[new_col] = data[feature].apply(lambda x: min(x, upper_bound))

        if result is not None:
            session.addDataFrame(new_name, result)

        if withImport:
            import_stmt = "\n".join(import_stmts)
            code = f"{import_stmt}\n\n{code}"

        return code, import_stmts

