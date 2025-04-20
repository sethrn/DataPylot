class UnivariatePlotGenerator:
    @staticmethod
    def generate(df, plot_type, params, withImport=False):
        import_stmts = ["import matplotlib.pyplot as plt"]

        if plot_type != "Pie Chart":
            import_stmts.append("import seaborn as sns")

        code = f"plt.figure(figsize=(8, 6))\n"
        
        style = params.get("Style")
        if style:
            code += f"sns.set_style('{style}')\n"

        grid = params.get("Grid Lines")
        if grid:
            code += "plt.grid(True)\n"

        match plot_type:
            case "Count Plot":
                code += (
                    f"sns.countplot(data={df}, x='{params['X Axis']}'"
                )
                if params.get("Color"):
                    code += f", color='{params['Color']}'"
                code += ")\n"

            case "Box Plot":
                code += (
                    f"sns.boxplot(data={df}, x='{params['X Axis']}'"
                )
                if params.get("Color"):
                    code += f", color='{params['Color']}'"
                code += ")\n"

            case "Histogram":
                code += (
                    f"sns.histplot(data={df}, x='{params['X Axis']}'"
                )
                if params.get("Color"):
                    code += f", color='{params['Color']}'"
                if params.get("Bins") is not None:
                    code += f", bins={params['Bins']}"
                if params.get("Density"):
                    code += ", stat='density'"
                if params.get("KDE Overlay"):
                    code += ", kde=True"
                code += ")\n"

            case "KDE Plot":
                code += (
                    f"sns.kdeplot(data={df}, x='{params['X Axis']}'"
                )
                if params.get("Color"):
                    code += f", color='{params['Color']}'"
                if params.get("Shade Area"):
                    code += ", fill=True"
                if params.get("Line Style"):
                    code += f", linestyle='{params['Line Style']}'"
                if params.get("Bandwidth") is not None:
                    code += f", bw_adjust={params['Bandwidth']}"
                code += ")\n"

            case "Pie Chart":
                code += (
                    f"counts = {df}['{params['Feature']}'].value_counts()\n"
                )
                
                if params.get("Color Palette"):
                    code += f"colors = sns.color_palette('{params['Color Palette']}')\n"
                else:
                    code += "colors = sns.color_palette()\n"

                if params.get("Explode Largest"):
                    code += (
                        "explode = [0.1 if i == counts.idxmax() else 0 for i in counts.index]\n"
                    )
                    explode_arg = ", explode=explode"
                else:
                    explode_arg = ""
                    
                autopct = "'%1.1f%%'" if params.get("Display Percentage") else "None"

                startangle = params.get("Start Angle")
                startangle_arg = f", startangle={startangle}" if startangle is not None else ""

                code += (
                    f"plt.pie(counts, labels=counts.index, colors=colors{explode_arg}, "
                    f"autopct={autopct}{startangle_arg})\n"
                )

        if params.get("Plot Title"):
            code += f"plt.title('{params['Plot Title']}')\n"

        if params.get("X Axis Label"):
            code += f"plt.xlabel('{params['X Axis Label']}')\n"
        elif "X Axis" in params:
            code += f"plt.xlabel('{params['X Axis']}')\n"

        if params.get("Y Axis Label"):
            code += f"plt.ylabel('{params['Y Axis Label']}')\n"
        elif "Y Axis" in params:
            code += f"plt.ylabel('{params['Y Axis']}')\n"

        if params.get("Label Rotation") is not None:
            code += f"plt.xticks(rotation={params['Label Rotation']})\n"

        code += "plt.show()"

        if withImport:
            code = "\n".join(import_stmts) + "\n\n" + code

        return code, import_stmts
