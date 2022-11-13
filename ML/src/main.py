from data import clean_dataset
from features import get_preprocessor
from features import Encoder, get_encoder
from sklearn.model_selection import train_test_split

RAW_DATA_PATH = "ML/data/raw/olx_house_price_Q122.csv"
INTERIM_DATA_PATH = "ML/data/interim/apartments.feather"

target = "price"


def main():
    df = clean_dataset(in_path=RAW_DATA_PATH, out_path=INTERIM_DATA_PATH)

    X = df.drop(target, axis=1)
    y = df[target]

    X, y = preprocessor.fit_transform(X, y)

    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.20, random_state=42
    )

    preprocessor = get_preprocessor(df=df)


if __name__ == "__main__":
    main()
