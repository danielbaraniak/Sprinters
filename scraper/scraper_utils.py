from random import randint
import requests
import csv
from typing import List, Dict

SEARCHED_FIELDS_OTD = {
    'offer_type': '"user_type":', 
    'floor': '"Floor_no":', 
    'area': '"Area":',
    'rooms': '"Rooms_num":', 
    'offer_type_of_building': 'ProperType":', 
    'market': '"MarketType":', 
    'longtitude': '"long":', 
    'latitude': '"lat":', 
    'price': '"Price":'
}

def get_random_number_from_range(left_boundary: int, right_boundary: int) -> int:
    return randint(left_boundary, right_boundary)

def get_flat_ox_data(link: str) -> dict:
    return {}

def get_flat_otd_data(link: str) -> dict:
    request = requests.get(link)
    str_request_data = str(request.content).split(',')
    filtered_data = {}

    for item in str_request_data:
        if SEARCHED_FIELDS_OTD['offer_type'] in item:
            filtered_data['offer_type'] = item.split(':')[1].strip('"}')
        if SEARCHED_FIELDS_OTD['floor'] in item:
            filtered_data['floor'] = item.split(':')[1].strip('[]"_flor')
        if SEARCHED_FIELDS_OTD['area'] in item:
            filtered_data['area'] = item.split(':')[2].strip('[]"_flor')
        if SEARCHED_FIELDS_OTD['rooms'] in item:
            filtered_data['rooms'] = item.split(':')[1].strip('[]"')
        if SEARCHED_FIELDS_OTD['offer_type_of_building'] in item:
            filtered_data['offer_type_of_building'] = item.split(':')[1].strip('[]"')
        if SEARCHED_FIELDS_OTD['market'] in item:
            filtered_data['market'] = item.split(':')[1].strip('[]"')
        if SEARCHED_FIELDS_OTD['longtitude'] in item:
            filtered_data['longtitude'] = item.split(':')[1].strip('[]"')
        if SEARCHED_FIELDS_OTD['latitude'] in item:
            filtered_data['latitude'] = item.split(':')[1].strip('[]"')
        if SEARCHED_FIELDS_OTD['price'] in item:
            filtered_data['price'] = item.split(':')[1].strip('[]"')
    
    return check_if_data_contains_all_fields(filtered_data)

def check_if_data_contains_all_fields(dict_data: dict) -> dict:
    for key, value in SEARCHED_FIELDS_OTD.items():
        if key not in dict_data.keys():
            dict_data[key] = 'null'
    return dict_data

def dump_csv_dict_data(data: List[Dict]):
    with open('artifact.csv', 'w') as csv_dump:
        writer = csv.DictWriter(csv_dump, SEARCHED_FIELDS_OTD.keys())
        writer.writeheader()
        writer.writerows(data)