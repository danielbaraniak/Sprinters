from flask import Flask, request
import joblib
import requests
import configparser

config = configparser.RawConfigParser()
config.read('settings.cfg')
details_dict = dict(config.items('sprinters-config'))
API_KEY = details_dict['API_KEY']

app = Flask(__name__)
fields = ['offer_type', 'floor', 'area', 'rooms', 'offer_type_of_building', 'market', 'longitude', 'latitude']
model = joblib.load('model.pkl')
featurizer_url = '69.69.69.69:5000/encode-data'

def _get_location_data(latitude, longitude):
    url = 'https://geocodeapi.p.rapidapi.com/GetNearestCities'
    location_fields = ['City', 'Population']
    querystring = {f'latitude':{latitude}, 'longitude':{longitude}, 'range':'0'}
    headers = {
        'X-RapidAPI-Key': API_KEY,
        'X-RapidAPI-Host': 'geocodeapi.p.rapidapi.com'
    }
    response = requests.request('GET', url, headers=headers, params=querystring)
    nearest_city = response[0]
    cleared_location = {location_field: nearest_city[location_field] for location_field in location_fields}
    return cleared_location

@app.route('/predict-price', methods=['POST'])
def predict_price():
    if request.method == 'POST':
        features = {}
        for field in fields:
            features[field] = request.form.get(field)
        location_features = _get_location_data(
            features['latitude'],
            features['longitude']
        )
        features = features | location_features
        ready_data = encoder.transform(features)
        prediction = model.predict(ready_data)
    return {
        'predicted_price': str(prediction[0])
    }

if __name__ == '__main__':
    app.run(debug=True)