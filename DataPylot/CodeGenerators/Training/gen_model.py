class ModelGenerator:
    @staticmethod
    def generate(params, session=None, withImport=False):
        imports = []
        code_lines = []

        df = params["df"]
        tech = params["tech"]
        target = params["target"]
        inputs = params["inputs"]
        model = params["model"]

        approach = params["approach"]
        kfolds = params["kfolds"]
        stratify = params["stratify"]
        test_size = params["test_size"]
    
        model_name = params["model_name"]
        hyperparams = params["hyperparams"]
    
        # Feature/target split
        quoted_inputs = ", ".join([f'"{col}"' for col in inputs])
        code_lines.append(f"X_{model_name} = {df}[[{quoted_inputs}]]")
        code_lines.append(f"y_{model_name} = {df}['{target}']")
        code_lines.append("")

        # Model instantiation (outside CV or within CV loop)
        model_code, model_import = ModelGenerator.get_model_instantiation(model, hyperparams, model_name)
        imports.append(model_import)

        if approach == "split":
            imports.append("from sklearn.model_selection import train_test_split")
            strat_arg = f", stratify=y_{model_name}" if stratify else ""
            code_lines += [
                f"X_train_{model_name}, X_test_{model_name}, y_train_{model_name}, y_test_{model_name} = train_test_split(",
                f"    X_{model_name}, y_{model_name}, test_size={test_size}, random_state=42{strat_arg})",
                f"{model_code}",
                f"{model_name}.fit(X_train_{model_name}, y_train_{model_name})",
                f"y_pred_{model_name} = {model_name}.predict(X_test_{model_name})",
            ]

            if tech == "class":
                imports.append("from sklearn.metrics import accuracy_score")
                code_lines.append(f"print('Accuracy:', accuracy_score(y_test_{model_name}, y_pred_{model_name}))")
            else:
                imports.append("from sklearn.metrics import r2_score")
                code_lines.append(f"print('R^2 Score:', r2_score(y_test_{model_name}, y_pred_{model_name}))")

        elif approach == "cv":
            if tech == "class":
                imports += [
                    "from sklearn.model_selection import StratifiedKFold",
                    "from sklearn.metrics import accuracy_score"
                ]
                code_lines += [
                    f"scores_list_{model_name} = []",
                    f"kf = StratifiedKFold(n_splits={kfolds}, shuffle=True, random_state=42)",
                    f"for train_index, test_index in kf.split(X_{model_name}, y_{model_name}):",
                    f"    X_train, X_test = X_{model_name}.iloc[train_index], X_{model_name}.iloc[test_index]",
                    f"    y_train, y_test = y_{model_name}.iloc[train_index], y_{model_name}.iloc[test_index]",
                    f"    {model_name} = {model}({', '.join(f'{k}={v}' for k, v in hyperparams.items())})",
                    f"    {model_name}.fit(X_train, y_train)",
                    f"    y_pred = {model_name}.predict(X_test)",
                    f"    scores_list_{model_name}.append(accuracy_score(y_test, y_pred))",
                    f"print('CV Accuracy per fold:', scores_list_{model_name})",
                    f"print('Mean CV Accuracy:', round(sum(scores_list_{model_name}) / {kfolds}, 4))"
                ]
            else:
                imports += [
                    "from sklearn.model_selection import KFold",
                    "from sklearn.metrics import r2_score"
                ]
                code_lines += [
                    f"scores_list_{model_name} = []",
                    f"kf = KFold(n_splits={kfolds}, shuffle=True, random_state=42)",
                    f"for train_index, test_index in kf.split(X_{model_name}):",
                    f"    X_train, X_test = X_{model_name}.iloc[train_index], X_{model_name}.iloc[test_index]",
                    f"    y_train, y_test = y_{model_name}.iloc[train_index], y_{model_name}.iloc[test_index]",
                    f"    {model_name} = {model}({', '.join(f'{k}={v}' for k, v in hyperparams.items())})",
                    f"    {model_name}.fit(X_train, y_train)",
                    f"    y_pred = {model_name}.predict(X_test)",
                    f"    scores_list_{model_name}.append(r2_score(y_test, y_pred))",
                    f"print('CV R^2 per fold:', scores_list_{model_name})",
                    f"print('Mean R^2:', round(sum(scores_list_{model_name}) / {kfolds}, 4))"
                ]

        if withImport:
            code_lines = imports + [""] + code_lines

        session.addModel(model_name, model)
        return "\n".join(code_lines), imports

    @staticmethod
    def get_model_instantiation(model_class, hyperparams, model_name):
        param_strs = []

        for name, value in hyperparams.items():
            param_strs.append(f"{name}={value}")

        param_str = ", ".join(param_strs) if param_strs else ""
        model_line = f"{model_name} = {model_class}({param_str})"

        return model_line, f"from sklearn.{ModelGenerator.get_model_module(model_class)} import {model_class}"

    @staticmethod
    def get_model_module(model_class):
        lookup = {
            # Regression
            "LinearRegression": "linear_model",
            "Ridge": "linear_model",
            "Lasso": "linear_model",
            "ElasticNet": "linear_model",
            "DecisionTreeRegressor": "tree",
            "RandomForestRegressor": "ensemble",
            "SVR": "svm",
            "KNeighborsRegressor": "neighbors",

            # Classification
            "LogisticRegression": "linear_model",
            "KNeighborsClassifier": "neighbors",
            "DecisionTreeClassifier": "tree",
            "RandomForestClassifier": "ensemble",
            "SVC": "svm",
            "GaussianNB": "naive_bayes",
            "CategoricalNB": "naive_bayes"
        }
        return lookup.get(model_class,"")
