class MultivariatePlotGenerator:
    @staticmethod
    def generate(df, plot, x, y, hue, title, rotation, color, withImport):
        import_stmts = [
            "import matplotlib.pyplot as plt",
            "import seaborn as sns"
        ]
        code = ""

        title_stmt = f"plt.title(\"{title}\")\n" if title else ""
        rot_stmt = f"plt.xticks(rotation={rotation})\n" if rotation != 0 else ""
        color_stmt = f", palette='{color}'" if color else ""

        match plot:
            case "Heatmap":
                color_stmt = f", cmap='{color}'" if color else ""
                code += (
                    f"correlation_matrix = {df}[{df}.select_dtypes(include='number').columns].corr()\n"
                    f"plt.figure(figsize=(10, 8))\n"
                    f"sns.heatmap(correlation_matrix, annot=True{color_stmt}, fmt='.2f', cbar=True)\n"
                    f"{title_stmt}"
                    f"plt.show()\n"
                )

            case "Pair Plot":
                hue_stmt = f", hue='{hue}'{color_stmt}" if hue else ""
                code += (
                    f"plt.figure(figsize=(10, 8))\n"
                    f"sns.pairplot({df}.select_dtypes(include='number'), diag_kind='kde'{hue_stmt})\n"
                    f"{title_stmt}"
                    f"plt.show()\n"
                )

            case "Violin Plot":
                hue_stmt = f", hue='{hue}'{color_stmt}" if hue else ""
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.violinplot(data={df}, x='{x}', y='{y}'{hue_stmt}, split=True)\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.show()\n"
                )

            case "Swarm Plot":
                hue_stmt = f", hue='{hue}'{color_stmt}" if hue else ""
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.swarmplot(data={df}, x='{x}', y='{y}'{hue_stmt})\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.show()\n"
                )

            case "Scatter Plot":
                hue_stmt = f", hue='{hue}'{color_stmt}" if hue else ""
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.scatterplot(data={df}, x='{x}', y='{y}'{hue_stmt})\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.show()\n"
                )

            case "Line Plot":
                hue_stmt = f", hue='{hue}'{color_stmt}" if hue else ""
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.lineplot(data={df}, x='{x}', y='{y}'{hue_stmt})\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.show()\n"
                )

        if withImport:
            imports_code = "\n".join(import_stmts)
            code = f"{imports_code}\n\n{code}"

        return code, import_stmts
