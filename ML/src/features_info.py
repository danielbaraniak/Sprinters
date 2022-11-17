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
    "price": "float32",
    "offer_type": "str",
    "floor": "float32",  # can be NaN
    "area": "float32",
    "rooms": "int8",
    "offer_type_of_building": "str",
    "market": "str",
    "longitude": "float32",
    "latitude": "float32",
    "city_name": "str",
    "population": "float32",
    "voivodeship": "str",
}

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

dummies_features = []

numeric_features = [
    "longitude",
    "latitude",
    "area",
    "population",
]

onehot_features = []

ordinal_features = [
    "rooms",
    "offer_type",
    "offer_type_of_building",
    "market",
    "city_name",
    "floor",
]


hparam_grid = {
    "n_estimators": [
        20,
        30,
        40,
        50,
        60,
        70,
        80,
        90,
        100,
        110,
        120,
        130,
        140,
        150,
        160,
        170,
        180,
        190,
    ],
    "max_depth": [None, 3, 5, 10],
    "min_samples_split": [2, 4, 6, 8, 10, 12, 14, 16, 18],
    "min_samples_leaf": [1, 3, 5, 7, 9, 11, 13, 15, 17, 19],
    "max_features": [0.5, 1, "sqrt", "log2"],
    "bootstrap": [True],
}
