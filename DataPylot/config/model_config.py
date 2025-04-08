MODEL_CONFIG = {
    "LinearRegression": [],
    "Ridge": [
        {"name": "alpha", "type": float, "default": 1.0, "allow_none": False}
    ],
    "Lasso": [
        {"name": "alpha", "type": float, "default": 1.0, "allow_none": False}
    ],
    "ElasticNet": [
        {"name": "alpha", "type": float, "default": 1.0, "allow_none": False},
        {"name": "l1_ratio", "type": float, "default": 0.5, "allow_none": False}
    ],
    "DecisionTreeRegressor": [
        {"name": "max_depth", "type": int, "default": None, "allow_none": True},
        {"name": "min_samples_split", "type": int, "default": 2, "allow_none": False}
    ],
    "RandomForestRegressor": [
        {"name": "n_estimators", "type": int, "default": 100, "allow_none": False},
        {"name": "max_depth", "type": int, "default": None, "allow_none": True}
    ],
    "SVR": [
        {"name": "C", "type": float, "default": 1.0, "allow_none": False},
        {"name": "kernel", "type": str, "default": "rbf", "allow_none": False}
    ],
    "KNeighborsRegressor": [
        {"name": "n_neighbors", "type": int, "default": 5, "allow_none": False}
    ],
    "LogisticRegression": [
        {"name": "C", "type": float, "default": 1.0, "allow_none": False},
        {"name": "penalty", "type": str, "default": "l2", "allow_none": False}
    ],
    "KNeighborsClassifier": [
        {"name": "n_neighbors", "type": int, "default": 5, "allow_none": False},
        {"name": "weights", "type": str, "default": "uniform", "allow_none": False}
    ],
    "DecisionTreeClassifier": [
        {"name": "max_depth", "type": int, "default": None, "allow_none": True},
        {"name": "min_samples_split", "type": int, "default": 2, "allow_none": False}
    ],
    "RandomForestClassifier": [
        {"name": "n_estimators", "type": int, "default": 100, "allow_none": False},
        {"name": "max_depth", "type": int, "default": None, "allow_none": True}
    ],
    "SVC": [
        {"name": "C", "type": float, "default": 1.0, "allow_none": False},
        {"name": "kernel", "type": str, "default": "rbf", "allow_none": False}
    ],
    "GaussianNB": [],
    "CategoricalNB": [
        {"name": "alpha", "type": float, "default": 1.0, "allow_none": False}
    ]
}
