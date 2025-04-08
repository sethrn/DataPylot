class VisualsGenerator:
    @staticmethod
    def generate(model_name, visual, withImport=False):
        code_lines = []
        import_lines = []

        if visual == "Prediction vs. Actual":
            import_lines += ["import matplotlib.pyplot as plt"]
            code_lines += [
                f"# Plotting Predicted vs Actual values for {model_name}",
                f"plt.figure(figsize=(8,5))",
                f"plt.scatter(y_test_{model_name}, y_pred_{model_name}, alpha=0.5)",
                f"plt.xlabel('Actual Values')",
                f"plt.ylabel('Predicted Values')",
                f"plt.title('Prediction vs Actual for {model_name}')",
                f"plt.grid(True)",
                f"plt.show()"
            ]

        elif visual == "Residual Plot":
            import_lines += ["import matplotlib.pyplot as plt"]
            code_lines += [
                f"# Plotting Residuals for {model_name}",
                f"residuals_{model_name} = y_test_{model_name} - y_pred_{model_name}",
                f"plt.figure(figsize=(8,5))",
                f"plt.scatter(y_pred_{model_name}, residuals_{model_name}, alpha=0.5)",
                f"plt.axhline(0, color='red', linestyle='--')",
                f"plt.xlabel('Predicted Values')",
                f"plt.ylabel('Residuals')",
                f"plt.title('Residual Plot for {model_name}')",
                f"plt.grid(True)",
                f"plt.show()"
            ]

        elif visual == "Confusion Matrix":
            import_lines += [
                "from sklearn.metrics import ConfusionMatrixDisplay",
                "import matplotlib.pyplot as plt"
            ]
            code_lines += [
                f"# Displaying Confusion Matrix for {model_name}",
                f"ConfusionMatrixDisplay.from_predictions(y_test_{model_name}, y_pred_{model_name})",
                f"plt.title('Confusion Matrix for {model_name}')",
                f"plt.show()"
            ]

        elif visual == "Feature Importances":
            import_lines += ["import matplotlib.pyplot as plt"]
            code_lines += [
                f"# Plotting Feature Importances for {model_name}",
                f"importances = {model_name}.feature_importances_",
                f"features = X_test_{model_name}.columns",
                f"indices = importances.argsort()[::-1]",
                f"plt.figure(figsize=(10,6))",
                f"plt.title('Feature Importances for {model_name}')",
                f"plt.bar(range(len(importances)), importances[indices])",
                f"plt.xticks(range(len(importances)), features[indices], rotation=90)",
                f"plt.tight_layout()",
                f"plt.show()"
            ]

        elif visual == "Tree Visualization":
            import_lines += [
                "from sklearn.tree import plot_tree",
                "import matplotlib.pyplot as plt"
            ]
            code_lines += [
                f"# Visualizing Decision Tree for {model_name}",
                f"plt.figure(figsize=(20,10))",
                f"plot_tree({model_name}, feature_names=X_train_{model_name}.columns, filled=True, fontsize=10)",
                f"plt.title('Decision Tree Visualization for {model_name}')",
                f"plt.show()"
            ]

        elif visual == "Classification Report":
            import_lines += [
                "from sklearn.metrics import classification_report"
            ]
            code_lines += [
                f"# Displaying Classification Report for {model_name}",
                f"print(classification_report(y_test_{model_name}, y_pred_{model_name}))"
            ]

        else:
            code_lines.append(f"# Unsupported visualization type: {visual}")

        code = "\n".join(code_lines)
        if withImport and import_lines:
            code = "\n".join(sorted(set(import_lines))) + "\n\n" + code

        return code, import_lines
