from random import randint
import requests
import csv
from typing import List, Dict
import pickle
import uuid

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

SEARCHED_FIELDS_OX = {
    'offer_type': ['"user_type":', 3],
    'floor': ['"Poziom', 3], 
    'area': ['"Powierzchnia', 3],
    'rooms': ['"rooms', 3], 
    'offer_type_of_building': ['"Rodzaj zabudowy', 3], 
    'market': ['"Rynek', 3], 
    'longtitude': ['"lon":', 0], 
    'latitude': ['"lat":', 0], 
    'price': ['"price"', 3]
}

def get_random_number_from_range(left_boundary: int, right_boundary: int) -> int:
    return randint(left_boundary, right_boundary)

def get_flat_ox_data(link: str) -> dict:
    request = requests.get(link)
    str_request_data = str(request.content).replace('\\', '').split(',')
    filtered_data = {}

    try:
        for key, value in SEARCHED_FIELDS_OX.items():
            for i, item in enumerate(str_request_data):
                if value[0] in item:
                    filtered_data[key] = str_request_data[i + value[1]]

        for item in filtered_data.keys():
            if 'floor' in item:
                filtered_data['floor'] = filtered_data['floor'].split(':')[1].strip('"}flor_')
            if 'area' in item:
                filtered_data['area'] = filtered_data['area'].split(':')[1].split(' ')[0].strip('"')
            if 'rooms' in item:
                filtered_data['rooms'] = filtered_data['rooms'].split(':')[1].split(' ')[0].strip('"')
            if 'offer_type_of_building' in item:
                filtered_data['offer_type_of_building'] = filtered_data['offer_type_of_building'].split(':')[1].strip('"}')
            if 'market' in item:
                filtered_data['market'] = filtered_data['market'].split(':')[1].strip('"}')
            if 'longtitude' in item:
                filtered_data['longtitude'] = filtered_data['longtitude'].split(':')[1]
            if 'latitude' in item:
                filtered_data['latitude'] = filtered_data['latitude'].split(':')[1]
            if 'price' in item:
                filtered_data['price'] = ''.join(filtered_data['price'].split(':')[1].split(' ')[0:2]).strip('"')
    except Exception:
        dump_scraped_data_to_pickle(str_request_data, str(uuid.uuid4()))

    return check_if_data_contains_all_fields(filtered_data, SEARCHED_FIELDS_OX)

def get_flat_otd_data(link: str) -> dict:
    request = requests.get(link)
    str_request_data = str(request.content).split(',')
    filtered_data = {}
    try:
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
    except Exception:
        dump_scraped_data_to_pickle(str_request_data, str(uuid.uuid4()))
    
    return check_if_data_contains_all_fields(filtered_data, SEARCHED_FIELDS_OTD)

def check_if_data_contains_all_fields(dict_data: dict, searched_fields: dict) -> dict:
    for key in searched_fields.keys():
        if key not in dict_data.keys():
            dict_data[key] = 'null'
    return dict_data

def dump_csv_dict_data(data: List[Dict]):
    with open('artifact.csv', 'w', newline='') as csv_dump:
        writer = csv.DictWriter(csv_dump, SEARCHED_FIELDS_OTD.keys())
        writer.writeheader()
        writer.writerows(data)

def dump_scraped_data_to_pickle(data: object, filename: str):
    with open(filename, 'wb') as output_file:
        pickle.dump(data, output_file)
    
def loadscraped_data_from_pickle(filename: str):
    with open(filename, 'rb') as input_file:
        loaded_data = pickle.load(input_file)
    return loaded_data
