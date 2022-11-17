from configparser import ConfigParser
from datetime import datetime
from os import path

import joblib
import numpy as np
from sklearn.compose import TransformedTargetRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline

from .data import features_target_split, get_dataset
from .features import get_preprocessor
from .features_info import target_column
from .models import search_model

config = ConfigParser()
config.read("settings.cfg")
config = dict(config["ml"])


model_dir = config["model_dir"]
raw_data_path = config["raw_dataset"]
custom_model: TransformedTargetRegressor = eval(config.get("custom_model", "None"))
target = target_column


def get_model_name(suffix: str):
    return f"{datetime.now():%Y-%m-%dT%H%M%S}{suffix}.pkl"


def get_model_path(model_dir, model_name):
    return path.join(model_dir, model_name)


def main():
    df = get_dataset(in_path=raw_data_path)
    X, y = features_target_split(df, target)

    preprocessor = get_preprocessor(df=X)
    X = preprocessor.transform(X)

    X_train, X_valid, y_train, y_valid = train_test_split(X, y, test_size=0.20)

    if custom_model is not None:
        model = custom_model
        model.fit(X_train, y_train)
    else:
        model = search_model(X_train, y_train)

    pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("model", model),
        ],
    )

    train_score = model.score(X_train, y_train)
    valid_score = model.score(X_valid, y_valid)

    model_path = get_model_path(
        model_dir, get_model_name(f"_[t{train_score:.3f}][v{valid_score:.3f}]")
    )

    print(f"{train_score=}; {valid_score=}")
    joblib.dump(pipeline, model_path)
