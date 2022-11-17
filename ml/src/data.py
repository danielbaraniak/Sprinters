import pandas as pd

from . import features_info


def get_dataset(in_path: str) -> pd.DataFrame:
    df_raw = pd.read_csv(in_path, dtype=features_info.types)
    df = df_raw[features_info.useful_columns]

    df = df.where(df["rooms"] <= 4, 4)

    return df


def features_target_split(df, target: str):
    X = df.drop(target, axis=1)
    y = df[target]
    return X, y
