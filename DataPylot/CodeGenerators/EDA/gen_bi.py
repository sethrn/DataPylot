class BivariatePlotGenerator:
    @staticmethod
    def generate(df, plot_type, params, withImport=False):
        import_stmts = [
            "import matplotlib.pyplot as plt",
            "import seaborn as sns"
        ]

        code = "plt.figure(figsize=(8, 6))\n"

        style = params.get("Plot Style")
        if style:
            code += f"sns.set_style('{style}')\n"

        if params.get("Grid Lines"):
            code += "plt.grid(True)\n"

        palette = f", palette='{params['Color Palette']}'" if params.get("Color Palette") else ""
        color = f", color='{params['Color']}'" if params.get("Color") else ""
        marker = f", marker='{params['Marker Style']}'" if params.get("Marker Style") else ""
        size = f", s={params['Point Size']}" if params.get("Point Size") is not None else ""
        rotation = params.get("Label Rotation", 0)
        rot_stmt = f"plt.xticks(rotation={rotation})\n" if rotation else ""

        title = params.get("Plot Title")
        if title:
            code += f"plt.title('{title}')\n"

        xlabel = params.get("X Axis Label") or params.get("X Axis")
        if xlabel:
            code += f"plt.xlabel('{xlabel}')\n"

        ylabel = params.get("Y Axis Label") or params.get("Y Axis")
        if ylabel:
            code += f"plt.ylabel('{ylabel}')\n"

        match plot_type:
            case "Grouped Count Plot":
                code += (
                    f"sns.countplot(data={df}, x='{params['X Axis']}', hue='{params['Hue']}'{palette})\n"
                )

            case "Grouped Box Plot":
                code += (
                    f"sns.boxplot(data={df}, x='{params['X Axis']}', hue='{params['Hue']}'{palette})\n"
                )

            case "Violin Plot":
                code += (
                    f"sns.violinplot(data={df}, x='{params['X Axis']}', y='{params['Y Axis']}'{color})\n"
                )

            case "Swarm Plot":
                code += (
                    f"sns.swarmplot(data={df}, x='{params['X Axis']}', y='{params['Y Axis']}'{color}{size}{marker})\n"
                )

            case "Scatter Plot":
                code += (
                    f"sns.scatterplot(data={df}, x='{params['X Axis']}', y='{params['Y Axis']}'{color}{size}{marker})\n"
                )

            case "Line Plot":
                code += (
                    f"sns.lineplot(data={df}, x='{params['X Axis']}', y='{params['Y Axis']}'{color}{marker})\n"
                )

        code += rot_stmt
        code += "plt.show()"

        if withImport:
            code = "\n".join(import_stmts) + "\n\n" + code

        return code, import_stmts
