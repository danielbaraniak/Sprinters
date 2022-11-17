from datetime import datetime

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

from .data import clean_dataset
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


def get_model_path(model_score):
    return path.join(
        model_dir,
        f"{datetime.now():%Y-%m-%d_%H:%M:%S}_score({model_score:.3f}).pkl",
    )


def split_features_target(df, target: str):
    X = df.drop(target, axis=1)
    y = df[target]
    return X, y


def main():
    df = clean_dataset(in_path=raw_data_path)
    X, y = split_features_target(df, target)

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
    print(f"{model_score=}")
    joblib.dump(pipeline, get_model_path(model_score))


if __name__ == "__main__":
    main()
