import json
import requests

from cerberus import Validator
import configparser
from flask import Flask, request
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import joblib

config = configparser.RawConfigParser()
config.read('settings.cfg')
settings = dict(config.items('sprinters-config'))

API_KEY = settings['api_key']
fields = ['offer_type', 'floor', 'area', 'rooms', 'offer_type_of_building', 'market', 'longitude', 'latitude']
model = joblib.load(settings['model_path'])
#encoder = joblib.load(settings['encoder_path'])

schema = {
    'offer_type': {'type': 'string', 'required': True},
    'floor': {'type': 'float', 'min': -1.00, 'required': True},
    'area': {'type': 'float', 'min': 10.00, 'required': True},
    'rooms': {'type': 'integer', 'min': 1, 'required': True},
    'offer_type_of_building': {'type': 'string', 'required': True},
    'market': {'type': 'string', 'required': True},
    'longitude': {'type': 'float', 'required': True},
    'latitude': {'type': 'float', 'required': True}
}
validator = Validator(schema)

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=['1/5seconds']
)

def _get_location_data(latitude, longitude):
    url = 'https://geocodeapi.p.rapidapi.com/GetNearestCities'
    location_fields = ['Population', 'CountryId']
    querystring = {f'latitude':{str(latitude)}, 'longitude':{str(longitude)}, 'range':'0'}
    headers = {
        'X-RapidAPI-Key': API_KEY,
        'X-RapidAPI-Host': 'geocodeapi.p.rapidapi.com'
    }
    response = requests.request('GET', url, headers=headers, params=querystring)
    nearest_city = json.loads(response.content)[0]
    cleared_location = {location_field: nearest_city[location_field] for location_field in location_fields}
    return cleared_location

@app.route('/predict-price', methods=['POST'])
def predict_price():
    if request.method == 'POST':
        data = json.loads(request.data)
        if not validator.validate(data):
            return validator.errors
        features = {}
        for field in fields:
            features[field] = data.get(field)
        location_features = _get_location_data(
            features['latitude'],
            features['longitude']
        )
        if location_features['CountryId'] != 'PL':
            return {'error': 'Please drop pin in boarders of Poland'}, 400
        features['population'] = location_features['Population']
        return 'XD'
        ready_data = encoder.transform(features)
        prediction = model.predict(ready_data)
    return {
        'predicted_price': str(prediction)
    }

if __name__ == '__main__':
    app.run(debug=True)