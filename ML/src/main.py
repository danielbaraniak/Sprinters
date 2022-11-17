from datetime import datetime

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

from .data import get_dataset, features_target_split
from .features import get_preprocessor
from .features_info import target_column
from .models import search_model
from configparser import ConfigParser
from os import path


config = ConfigParser()
config.read("ML/settings.cfg")
config = dict(config["ml"])


model_dir = config["model_dir"]
raw_data_path = config["raw_dataset"]
custom_model: RandomForestRegressor = eval(config.get("custom_model", "None"))
target = target_column


def get_model_name(model_score):
    return f"{datetime.now():%Y-%m-%d_%H:%M:%S}_score({model_score:.3f}).pkl"


def get_model_path(model_dir, model_name):
    return path.join(model_dir, model_name)


def main():
    df = get_dataset(in_path=raw_data_path)
    X, y = features_target_split(df, target)

    preprocessor = get_preprocessor(df=X)
    X = preprocessor.transform(X)

    if custom_model is not None:
        model = custom_model
        model.fit(X, y)
    else:
        model = search_model(X, y)

    pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("model", model),
        ],
    )

    model_score = model.score(X, y)
    model_path = get_model_path(model_dir, get_model_name(model_score))

    print(f"{model_score=}")
    joblib.dump(pipeline, model_path)


if __name__ == "__main__":
    main()
