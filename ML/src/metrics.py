import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def print_score(m, *, X_train, y_train, X_valid, y_valid):
    res = {"r2_train": m.score(X_train, y_train), "r2_valid": m.score(X_valid, y_valid)}
    print(res)


def plot_importances(m, columns):
    importances = m.feature_importances_
    std = np.std([tree.feature_importances_ for tree in m], axis=0)

    forest_importances = pd.Series(importances, index=columns)

    fig, ax = plt.subplots()
    forest_importances.plot.bar(yerr=std, ax=ax)
    ax.set_title("Feature importances using MDI")
    ax.set_ylabel("Mean decrease in impurity")
    fig.tight_layout()
