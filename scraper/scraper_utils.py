import requests
import csv
import pickle
import re
import json

from random import randint
from typing import List, Dict

def get_random_number_from_range(left_boundary: int, right_boundary: int) -> int:
    return randint(left_boundary, right_boundary)

def get_flat_ox_data(link: str):
    response = requests.get(link)    
    text = response.content.decode('utf-8')
    m = re.search(r'(?<=window.__PRERENDERED_STATE__= ")(.*?)(?="cookies\\":{}})', text)
    data = json.loads(m.group(0).replace('\\','')[:-1] + '}')

    TARGET_FIELDS_OX_TRANSLATION = {
        'price': data['ad']['ad']['price']['regularPrice']['value'],
        "offer_type": '',
        "floor": data['ad']['ad']['params'][1]['normalizedValue'],
        "area": data['ad']['ad']['params'][5]['normalizedValue'],
        "rooms": data['ad']['ad']['params'][6]['normalizedValue'],
        "offer_type_of_building": data['ad']['ad']['params'][4]['normalizedValue'],
        "market": data['ad']['ad']['params'][3]['normalizedValue'],
        "longtitude": data['ad']['ad']['map']['lon'],
        "latitude": data['ad']['ad']['map']['lat'],
        'city_name': data['ad']['ad']['location']['cityName'],
        'build_year': ''
    }

    return TARGET_FIELDS_OX_TRANSLATION

def get_flat_otd_data(link: str) -> dict:
    response = requests.get(link)    
    text = response.content.decode('utf-8')
    m = re.search(r'<script id="__NEXT_DATA__".*>(.*)</script>', text)
    data = json.loads(m.groups()[0])
    target = {
        **data['props']['pageProps']['ad']['target'], **data['props']['pageProps']['adTrackingData']
        }

    SEARCHED_FIELDS_OTD_TRANSLATION = {
        'price': 'ad_price',
        "offer_type": 'user_type',
        "floor": 'Floor_no',
        "area": 'Area',
        "rooms": 'Rooms_num',
        "offer_type_of_building": 'ProperType',
        "market": 'market',
        "longtitude": 'long',
        "latitude": 'lat',
        'city_name': 'city_name',
        'build_year': 'Build_year'
    }

    result = {}
    for target_key, raw_key  in SEARCHED_FIELDS_OTD_TRANSLATION.items():
        v = target.get(raw_key)
        if isinstance(v, list):
            v = v[0]
        result[target_key] = v
    
    return check_if_data_contains_all_fields(result, SEARCHED_FIELDS_OTD_TRANSLATION)

def check_if_data_contains_all_fields(dict_data: dict, searched_fields: dict) -> dict:
    for key in searched_fields.keys():
        if key not in dict_data.keys():
            dict_data[key] = 'null'
    return dict_data

def dump_csv_dict_data(data: List[Dict]):
    with open('ml/data/raw/artifact.csv', 'w', newline='') as csv_dump:
        DICT_VALUES = [
            'price',
            "offer_type",
            "floor",
            "area",
            "rooms",
            "offer_type_of_building",
            "market",
            "longtitude",
            "latitude",
            'city_name',
            'build_year'
        ]
        writer = csv.DictWriter(csv_dump, DICT_VALUES)
        writer.writeheader()
        writer.writerows(data)

def dump_scraped_data_to_pickle(data: object, filename: str):
    with open(filename, 'wb') as output_file:
        pickle.dump(data, output_file)
    
def loadscraped_data_from_pickle(filename: str):
    with open(filename, 'rb') as input_file:
        loaded_data = pickle.load(input_file)
    return loaded_data
