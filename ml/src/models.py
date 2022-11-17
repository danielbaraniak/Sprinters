import numpy as np
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import RandomizedSearchCV

from . import features_info

hparam_grid = {"regressor__" + k: v for k, v in features_info.hparam_grid.items()}


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
