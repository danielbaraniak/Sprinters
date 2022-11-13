import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import (
    StandardScaler,
    OneHotEncoder,
    OrdinalEncoder,
    FunctionTransformer,
)

columns_order = [
    "offer_type",
    "floor",
    "area",
    "rooms",
    "offer_type_of_building",
    "market",
    "longitude",
    "latitude",
    "city_name",
    "population",
    "voivodeship",
]

dummies_features = [
    "rooms",
    "floor",
]

numeric_features = ["longitude", "latitude", "area", "population"]

onehot_features = []

ordinal_features = [
    "offer_type",
    "offer_type_of_building",
    "market",
    "city_name",
    "voivodeship",
]


def dummies(df_e):
    df_e = pd.get_dummies(df_e)
    df_e.fillna(value=-2.0, inplace=True)
    return df_e


def dummies_feature_names_out(_, input_features: list[str]) -> list:
    result = []
    for f in input_features:
        result.append(f)
        result.append(f + "_na")

    return result


numeric_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="median")),
        # ("scaler", StandardScaler()),
    ]
)

onehot_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="constant",
                fill_value="missing",
            ),
        ),
        (
            "onehot",
            OneHotEncoder(
                handle_unknown="infrequent_if_exist",
                max_categories=10,
            ),
        ),
    ]
)

ordinal_transformer = Pipeline(
    steps=[
        (
            "imputer",
            SimpleImputer(
                strategy="constant",
                fill_value="missing",
            ),
        ),
        (
            "ordinal",
            OrdinalEncoder(encoded_missing_value=-2.0),
        ),
    ]
)

dummies_transformer = FunctionTransformer(
    dummies, feature_names_out=dummies_feature_names_out
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("one_hot", onehot_transformer, onehot_features),
        # ("dummies", dummies_transformer, dummies_features),
        ("ordinal", ordinal_transformer, ordinal_features),
    ],
    n_jobs=-1,
    remainder="passthrough",
)


def get_preprocessor(
    *, dataset_path: str = None, df: pd.DataFrame = None
) -> ColumnTransformer:
    """
    dataset_path: path to the file with serialized dataset (ML/data/interim/...)
    df: dataframe to be used for fitting.
    """
    if dataset_path:
        df = pd.read_feather(dataset_path)
        df.drop(["index"], axis=1, inplace=True)
        print(df.head())

    if df is None:
        raise ValueError("Empty dataframe. Specify 'dataset_path' or 'df'.")

    preprocessor.fit(df)
    return preprocessor


def featurize(preprocessor: ColumnTransformer, data: dict) -> np.ndarray:
    X = pd.DataFrame({k: [v] for k, v in data.items()})
    return preprocessor.transform(X)
