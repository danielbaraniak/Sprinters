from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import pickle

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
fields = ['offer_type', 'floor', 'area', 'rooms', 'offer_type_of_building', 'market', 'voivodeship']

model = pickle.load(open('model-name-path', 'rb'))

@app.route('/')
@cross_origin
def home_page():
    return 'Amazing home page'

@app.route('/predict-price', methods=['POST'])
def predict_price():
    if request.method == 'POST':
        features = []
        data = request.form
        for field in fields:
            features.append(data.get(field))
        final_features = ([features])
        prediction = model.predict(final_features)
    return jsonify(str(f'Predicted price: {prediction[0]}'))

if __name__ == '__main__':
    app.run(debug=True)