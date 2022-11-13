import numpy as np
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV


hparam_grid = {
    "n_estimators": np.arange(20, 200, 10),
    "max_depth": [None, 3, 5, 10],
    "min_samples_split": np.arange(2, 20, 2),
    "min_samples_leaf": np.arange(1, 20, 2),
    "max_features": [0.5, 1, "sqrt", "log2"],
    "bootstrap": [True],
}

hparam_grid = {"regressor__" + k: v for k, v in hparam_grid.items()}


def search_model(X, y):
    reg = RandomForestRegressor(n_jobs=-1)
    ttr = TransformedTargetRegressor(
        regressor=reg,
        func=np.log,
        inverse_func=np.exp,
        check_inverse=False,
    )

    opt = RandomizedSearchCV(
        ttr,
        param_distributions=hparam_grid,
        n_iter=50,
        cv=5,
        verbose=True,
        n_jobs=-1,
    )

    opt.fit(X, y)

    return opt.best_estimator_
