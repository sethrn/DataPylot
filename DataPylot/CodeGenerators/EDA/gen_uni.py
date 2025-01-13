class UnivariatePlotGenerator:
    @staticmethod
    def generate(df, feature, plot, title, rotation, color, withImport):
        import_stmts = [
            "import matplotlib.pyplot as plt",
            "import seaborn as sns"
        ]
        code = ""

        color_stmt = f", color='{color}'" if color else ""
        title_stmt = f"plt.title(\"{title}\")\n" if title else ""
        rot_stmt = f"plt.xticks(rotation={rotation})\n" if rotation != 0 else ""

        match plot:
            case 'Pie Chart':
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"counts = {df}['{feature}'].value_counts()\n"
                    f"colors = sns.color_palette()\n"
                    f"plt.pie(counts, labels=counts.index, colors=colors, autopct='%1.1f%%', startangle={rotation})\n"
                    f"{title_stmt}"
                    f"plt.show()"
                )
            case 'Histogram':
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.histplot(data={df}, x='{feature}'{color_stmt}, kde=False)\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.xlabel(\"{feature}\")\n"
                    f"plt.ylabel('Frequency')\n"
                    f"plt.show()"
                )
            case 'Kernel Density Estimate':
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.kdeplot(data={df}, x='{feature}'{color_stmt}, fill=True)\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.xlabel(\"{feature}\")\n"
                    f"plt.ylabel('Density')\n"
                    f"plt.show()"
                )
            case 'Boxplot':
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.boxplot(data={df}, x='{feature}'{color_stmt})\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.xlabel(\"{feature}\")\n"
                    f"plt.ylabel('Value')\n"
                    f"plt.show()"
                )
            case 'Countplot':
                code += (
                    f"plt.figure(figsize=(8, 6))\n"
                    f"sns.countplot(data={df}, x='{feature}'{color_stmt})\n"
                    f"{title_stmt}"
                    f"{rot_stmt}"
                    f"plt.xlabel(\"{feature}\")\n"
                    f"plt.ylabel('Count')\n"
                    f"plt.show()"
                )

        if withImport:
            imports_code = "\n".join(import_stmts)
            code = f"{imports_code}\n\n{code}"

        return code, import_stmts
