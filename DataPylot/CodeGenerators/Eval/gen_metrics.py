class MetricsGenerator:
    @staticmethod
    def generate(model_name, metrics, withImport=False):
        code = []
        imports = []

        metric_map = {
            "Accuracy": {
                "import": "from sklearn.metrics import accuracy_score",
                "code": f"print('Accuracy:', accuracy_score(y_test_{model_name}, y_pred_{model_name}))"
            },
            "Classification Report": {
                "import": "from sklearn.metrics import classification_report",
                "code": f"print(classification_report(y_test_{model_name}, y_pred_{model_name}))"
            },
            "R2 Score": {
                "import": "from sklearn.metrics import r2_score",
                "code": f"print('R^2 Score:', r2_score(y_test_{model_name}, y_pred_{model_name}))"
            },
            "Mean Absolute Error": {
                "import": "from sklearn.metrics import mean_absolute_error",
                "code": f"print('MAE:', mean_absolute_error(y_test_{model_name}, y_pred_{model_name}))"
            },
            "Mean Square Error": {
                "import": "from sklearn.metrics import mean_squared_error",
                "code": f"print('MSE:', mean_squared_error(y_test_{model_name}, y_pred_{model_name}))"
            },
            "Median Absolute Error": {
                "import": "from sklearn.metrics import median_absolute_error",
                "code": f"print('Median AE:', median_absolute_error(y_test_{model_name}, y_pred_{model_name}))"
            }
        }

        for metric in metrics:
            entry = metric_map.get(metric)
            if entry:
                code.append(f"# Displaying {metric} for {model_name}")
                code.append(entry["code"])
                imports.append(entry["import"])
            else:
                code.append(f"# Unsupported metric: {metric}")

        imports = list(sorted(set(imports)))

        code = "\n".join(code)
        if withImport and imports:
            import_block = "\n".join(imports)
            code = import_block + "\n\n" + code

        return code, imports

