from flask import Flask, request
import joblib
import requests

app = Flask(__name__)
fields = ['offer_type', 'floor', 'area', 'rooms', 'offer_type_of_building',
    'market', 'voivodeship', 'city_name', 'population', 'longitude', 'latitude']

model = joblib.load('model.pkl')
featurizer_url = '69.69.69.69:5000'

@app.route('/predict-price', methods=['POST'])
def predict_price():
    if request.method == 'POST':
        features = {}
        for field in fields:
            features[field] = request.form.get(field)
        response = requests.post(url=featurizer_url, data=features)
        prediction = model.predict(response.data)
    return {
        'predicted_price': str(prediction[0])
    }

if __name__ == '__main__':
    app.run(debug=True)