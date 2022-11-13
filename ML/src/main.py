from data import clean_dataset
from features import Encoder, get_encoder

RAW_DATA_PATH = "ML/data/raw/olx_house_price_Q122.csv"
INTERIM_DATA_PATH = "ML/data/interim/apartments.feather"


def main():
    df = clean_dataset(in_path=RAW_DATA_PATH, out_path=INTERIM_DATA_PATH)


if __name__ == "__main__":
    main()
