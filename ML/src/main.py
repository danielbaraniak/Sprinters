from datetime import datetime

import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline

from data import clean_dataset
from features import get_preprocessor
from models import search_model


RAW_DATA_PATH = "ML/data/raw/olx_house_price_Q122.csv"
INTERIM_DATA_PATH = "ML/data/interim/apartments.feather"
MODEL_OUTPUT_PATH = "ML/models/" + str(datetime.now()) + ".pkl"

target = "price"


def main():
    df = clean_dataset(in_path=RAW_DATA_PATH, out_path=INTERIM_DATA_PATH)

    X = df.drop(target, axis=1)
    y = df[target]

    preprocessor = get_preprocessor(df=X)

    X = preprocessor.transform(X)

    model = RandomForestRegressor(max_features="log2", n_estimators=180, n_jobs=-1)
    model.fit(X, y)
    # model = search_model(X, y)

    print(f"{model.score(X, y)=}")

    pipeline = Pipeline(
        steps=[
            ("preprocessing", preprocessor),
            ("model", model),
        ],
    )

    joblib.dump(pipeline, MODEL_OUTPUT_PATH)


if __name__ == "__main__":
    main()
