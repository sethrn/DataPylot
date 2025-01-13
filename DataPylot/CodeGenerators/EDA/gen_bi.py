class BivariatePlotGenerator:
    @staticmethod
    def generate(df, plot, x, y, title, rotation, color, withImport):
        import_stmts = [
            "import matplotlib.pyplot as plt",
            "import seaborn as sns"
        ]
        code = ""

        title_stmt = f"plt.title(\"{title}\")\n" if title else ""
        rot_stmt = f"plt.xticks(rotation={rotation})\n" if rotation != 0 else ""
        color_stmt = f", palette='{color}'" if color else ""

        match plot:
            case "Violin Plot":
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.violinplot(data={df}, x='{x}', y='{y}', hue='{x}'{color_stmt})\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.show()"
                )
            case "Swarm Plot":
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.swarmplot(data={df}, x='{x}', y='{y}', hue='{x}'{color_stmt})\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.show()"
                )
            case "Scatter Plot":
                color_stmt = f", color='{color}'" if color else ""
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.scatterplot(data={df}, x='{x}', y='{y}'{color_stmt})\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.show()"
                )
            case "Line Plot":
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.lineplot(data={df}, x='{x}', y='{y}'{color_stmt})\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.show()"
                )
            case "Grouped Count Plot":
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.countplot(data={df}, x='{x}', hue='{y}'{color_stmt})\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.show()"
                )
            case "Grouped Box Plot":
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.boxplot(data={df}, x='{x}', hue='{y}'{color_stmt})\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.show()"
                )

        if withImport:
            imports_code = "\n".join(import_stmts)
            code = f"{imports_code}\n\n{code}"

        return code, import_stmts