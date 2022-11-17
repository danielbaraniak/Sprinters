from datetime import datetime

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

from .data import clean_dataset
from .features import get_preprocessor
from .models import search_model
from configparser import ConfigParser
from os import path


config = ConfigParser()
config.read("ML/settings.cfg")


model_output_path = path.join(
    config["ml"]["model_dir"],
    str(datetime.now().strftime("%Y-%m-%d_%H:%M:%S")) + ".pkl",
)

target = "price"
raw_data_path = config["ml"]["raw_dataset"]
custom_model: RandomForestRegressor = eval(config["ml"].get("custom_model", "None"))


def main():
    df = clean_dataset(in_path=raw_data_path)

    X = df.drop(target, axis=1)
    y = df[target]

    preprocessor = get_preprocessor(df=X)
    X = preprocessor.transform(X)

    if custom_model is not None:
        model = custom_model
        model.fit(X, y)
    else:
        model = search_model(X, y)

    print(f"{model.score(X, y)=}")

    pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("model", model),
        ],
    )

    joblib.dump(pipeline, model_output_path)


if __name__ == "__main__":
    main()
