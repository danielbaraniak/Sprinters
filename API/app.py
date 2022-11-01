from flask import Flask, request
from sklearn.preprocessing import OrdinalEncoder
import numpy as np
import pickle
import joblib

app = Flask(__name__)
fields = ['offer_type', 'floor', 'area', 'rooms', 'offer_type_of_building', 'market', 'voivodeship']
categorical_features = ['offer_type', 'offer_type_of_building', 'market', 'voivodeship']
encoder = OrdinalEncoder(dtype=np.int32, encoded_missing_value=-2)

def encode_data(features):
    features = encoder.fit_transform(features)
    return features

#model = pickle.load(open('model.pkl', 'rb'))
model = joblib.load('model.pkl')

@app.route('/predict-price', methods=['POST'])
def predict_price():
    if request.method == 'POST':
        features = []
        data = request.form
        for field in fields:
            print(f'Now adding {field}')
            feature = []
            feature.append(field)
            feature.append(data.get(field))
            features.append(feature)
        print(f'Features before encoding {features}')
        features = encode_data(features)
        print(f'Features after encoding {features}')
        final_features = (features)
        prediction = model.predict(final_features)
    return {
        'predicted_price': str(prediction[0])
    }

if __name__ == '__main__':
    app.run(debug=True)