MODEL_EVAL_CONFIG = {
    "LinearRegression": {
        "type": "regression",
        "metrics": ["R2 Score", "Mean Absolute Error", "Mean Squared Error", "Median Absolute Error"],
        "visuals": ["Residual Plot", "Prediction vs. Actual"]
    },
    "Ridge": {
        "type": "regression",
        "metrics": ["R2 Score", "Mean Absolute Error", "Mean Squared Error", "Median Absolute Error"],
        "visuals": ["Residual Plot", "Prediction vs. Actual"]
    },
    "Lasso": {
        "type": "regression",
        "metrics": ["R2 Score", "Mean Absolute Error", "Mean Squared Error", "Median Absolute Error"],
        "visuals": ["Residual Plot", "Prediction vs. Actual"]
    },
    "ElasticNet": {
        "type": "regression",
        "metrics": ["R2 Score", "Mean Absolute Error", "Mean Squared Error", "Median Absolute Error"],
        "visuals": ["Residual Plot", "Prediction vs. Actual"]
    },
    "DecisionTreeRegressor": {
        "type": "regression",
        "metrics": ["R2 Score", "Mean Absolute Error", "Mean Squared Error"],
        "visuals": ["Prediction vs. Actual", "Tree Visualization", "Feature Importances"]
    },
    "SVR": {
        "type": "regression",
        "metrics": ["R2 Score", "Mean Absolute Error", "Mean Squared Error"],
        "visuals": ["Prediction vs. Actual"]
    },
    "KNeighborsRegressor": {
        "type": "regression",
        "metrics": ["R2 Score", "Mean Absolute Error", "Mean Squared Error"],
        "visuals": ["Prediction vs. Actual"]
    },


    "LogisticRegression": {
        "type": "classification",
        "metrics": ["Accuracy", "Classification Report"],
        "visuals": ["Confusion Matrix", "ROC Curve"]
    },
    "KNeighborsClassifier": {
        "type": "classification",
        "metrics": ["Accuracy", "Classification Report"],
        "visuals": ["Confusion Matrix"]
    },
    "DecisionTreeClassifier": {
        "type": "classification",
        "metrics": ["Accuracy", "Classification Report"],
        "visuals": ["Confusion Matrix", "Tree Visualization", "Feature Importances"]
    },
    "RandomForestClassifier": {
        "type": "classification",
        "metrics": ["Accuracy", "Classification Report"],
        "visuals": ["Confusion Matrix", "Feature Importances"]
    },
    "SVC": {
        "type": "classification",
        "metrics": ["Accuracy", "Classification Report"],
        "visuals": ["Confusion Matrix", "ROC Curve"]
    },
    "GaussianNB": {
        "type": "classification",
        "metrics": ["Accuracy", "Classification Report"],
        "visuals": ["Confusion Matrix"]
    },
    "CategoricalNB": {
        "type": "classification",
        "metrics": ["Accuracy", "Classification Report"],
        "visuals": ["Confusion Matrix"]
    }
}
