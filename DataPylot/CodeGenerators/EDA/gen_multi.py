class MultivariatePlotGenerator:
    @staticmethod
    def generate(df, plot_type, params, withImport=False):
        import_stmts = [
            "import matplotlib.pyplot as plt",
            "import seaborn as sns"
        ]
        code = "plt.figure(figsize=(8, 6))\n"

        if params.get("Style"):
            code += f"sns.set_style('{params['Style']}')\n"

        if params.get("Show Legend") is False:
            legend_stmt = "plt.legend().remove()\n"
        else:
            legend_stmt = ""

        if params.get("Grid Lines"):
            code += "plt.grid(True)\n"

        palette = f", palette='{params['Palette']}'" if params.get("Palette") else ""
        color = f", color='{params['Color']}'" if params.get("Color") else ""
        cmap = f", cmap='{params['Color Map']}'" if params.get("Color Map") else ""
        marker = f", marker='{params['Marker Style']}'" if params.get("Marker Style") else ""
        linestyle = f", linestyle='{params['Line Style']}'" if params.get("Line Style") else ""
        alpha = f", alpha={params['Alpha (Transparency)']}" if params.get("Alpha (Transparency)") is not None else ""
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
            case "Grouped Violin Plot":
                code += (
                    f"sns.violinplot(data={df}, x='{params['X Axis']}', y='{params['Y Axis']}', hue='{params['Hue']}'{palette}, split=True)\n"
                    f"{rot_stmt}{legend_stmt}"
                )

            case "Grouped Swarm Plot":
                code += (
                    f"sns.swarmplot(data={df}, x='{params['X Axis']}', y='{params['Y Axis']}', hue='{params['Hue']}'{palette}{size}{alpha})\n"
                    f"{rot_stmt}{legend_stmt}"
                )

            case "Grouped Scatter Plot":
                code += (
                    f"sns.scatterplot(data={df}, x='{params['X Axis']}', y='{params['Y Axis']}', hue='{params['Hue']}'{palette}{marker}{size}{alpha})\n"
                    f"{rot_stmt}{legend_stmt}"
                )

            case "Grouped Line Plot":
                code += (
                    f"sns.lineplot(data={df}, x='{params['X Axis']}', y='{params['Y Axis']}', hue='{params['Hue']}'{marker}{linestyle}{alpha})\n"
                    f"{rot_stmt}{legend_stmt}"
                )

            case "Heatmap":
                method = params.get("Correlation Method", "pearson")
                annot = f", annot=True" if params.get("Annotate Values", True) else ""
                code += (
                    f"correlation_matrix = {df}[{df}.select_dtypes(include='number').columns].corr(method='{method}')\n"
                    f"sns.heatmap(correlation_matrix{annot}{cmap}, fmt='.2f', cbar=True)\n"
                )

            case "Pair Plot":
                hue_stmt = f", hue='{params['Hue']}'" if params.get("Hue") else ""
                kind_stmt = f", kind='{params['Kind']}'" if params.get("Kind") else ""
                code += (
                    f"sns.pairplot({df}.select_dtypes(include='number'){hue_stmt}{palette}{kind_stmt})\n"
                )

        code += "plt.show()"

        if withImport:
            imports_code = "\n".join(import_stmts)
            code = f"{imports_code}\n\n{code}"

        return code, import_stmts
