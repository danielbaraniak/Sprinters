import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import (
    FunctionTransformer,
    OneHotEncoder,
    OrdinalEncoder,
    StandardScaler,
)

from . import features_info


def _dummies(df_e):
    df_e = pd.get_dummies(df_e)
    df_e.fillna(value=-2.0, inplace=True)
    return df_e


def _dummies_feature_names_out(transformer, input_features: list[str]) -> list:
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
            "ordinal",
            OrdinalEncoder(encoded_missing_value=-2.0),
        ),
    ]
)

dummies_transformer = FunctionTransformer(
    _dummies, feature_names_out=_dummies_feature_names_out
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, features_info.numeric_features),
        ("one_hot", onehot_transformer, features_info.onehot_features),
        ("dummies", dummies_transformer, features_info.dummies_features),
        ("ordinal", ordinal_transformer, features_info.ordinal_features),
    ],
    n_jobs=-1,
)


def get_preprocessor(df: pd.DataFrame) -> ColumnTransformer:

    preprocessor.fit(df.reindex(columns=features_info.columns_order))
    return preprocessor


def featurize(preprocessor: ColumnTransformer, data: dict) -> np.ndarray:
    X = pd.DataFrame({k: [v] for k, v in data.items()})
    return preprocessor.transform(X)
