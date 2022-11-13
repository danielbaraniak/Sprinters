import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder, OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.impute import SimpleImputer

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

ordinal_features = [
    "city_name",
    "voivodeship",
]

onehot_features = [
    "offer_type",
    "offer_type_of_building",
    "market",
]


class Encoder:
    def __init__(self) -> None:
        self.transformer = make_column_transformer(
            (OrdinalEncoder(dtype=np.int32), ordinal_features),
            (OneHotEncoder(dtype=np.int8), onehot_features),
            (
                SimpleImputer(
                    strategy="constant",
                    fill_value=-2.0,
                ),
                ["floor"],
            ),
            remainder="passthrough",
        )

    def fit(self, df: pd.DataFrame):
        self.transformer.fit(df)

    def transform(self, df: pd.DataFrame, out_path: str = None):
        df.reindex(columns=columns_order)
        df = self.transformer.transform(df)
        if out_path:
            df.reset_index().to_feather(out_path)

        return df

    def featurize(self, data: dict) -> np.ndarray:
        d = {k: [v] for k, v in data.items()}
        df = pd.DataFrame(d)

        return self.transform(df)


def get_encoder(dataset_path: str) -> Encoder:
    """
    dataset_path: path to the file with serialized dataset (ML/data/interim/...)
    """
    df = pd.read_feather(dataset_path)
    df.drop(["index"], axis=1, inplace=True)
    print(df.head())
    enc = Encoder()
    enc.fit(df)
    return enc
