# About Dataset

Analyses of the pricing and brand based on [OLX Portal](https://www.olx.pl/nieruchomosci/mieszkania/)

- source: [https://www.kaggle.com/datasets/g1llar/poland-olx-house-price-q122](https://www.kaggle.com/datasets/g1llar/poland-olx-house-price-q122)

- csv file: [ml/data/raw/olx_house_price_Q122.csv](/ml/data/raw/olx_house_price_Q122.csv)

## Features description

- `offer_title`: offer title
- `price`: price in PLN
- `price_per_meter`: price in PLN for square meter
- `offer_type`: Estate Agency, Private, ...
- `floor`: floor number for -1 --> basement, 0 --> Ground Floor, 10 --> floor 10+, 11 --> attic
- `area`: area in square meters
- `rooms`: number of rooms for 4 --> rooms 4+
- `offer_type_of_building`: Housing Block, Apartment Building, ...
- `market`: new, aftermarket, ...
- `city_name`: name of city where home is
- `voivodeship`: name of voivodeship where home is
- `month`: data download month
- `year`: data download year
- `population`: city population where home is
- `longitude`, `latitude`: city coordinates

File variables `dummies_features`, `numeric_features`, `onehot_features`, and `ordinal_features` in [`ml.src.features_info`](/ml/src/features_info.py) describe which features are used for training and what method of transformation will be applied.
