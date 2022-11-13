import numpy as np
import pandas as pd

useful_columns = [
    "price",
    "offer_type",
    "floor",  # can be NaN
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

types = {
    "price": np.float32,
    "offer_type": "str",
    "floor": np.float32,  # can be NaN
    "area": np.float32,
    "rooms": np.int8,
    "offer_type_of_building": "str",
    "market": "str",
    "longitude": np.float32,
    "latitude": np.float32,
    "city_name": "str",
    "population": np.float32,
    "voivodeship": "str",
}


def clean_dataset(in_path: str, out_path: str = None) -> pd.DataFrame:
    df_raw = pd.read_csv(in_path, dtype=types)
    df = df_raw[useful_columns]
    df = df.dropna(subset=["area", "offer_type_of_building"])
    df = df.where(df["rooms"] <= 4, 4)

    if out_path:
        df.reset_index().to_feather(out_path)

    return df
