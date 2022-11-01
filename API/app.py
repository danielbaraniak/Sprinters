from flask import Flask, request
import pickle

app = Flask(__name__)
fields = ['offer_type', 'floor', 'area', 'rooms', 'offer_type_of_building', 'market', 'voivodeship']

model = pickle.load(open('trained-model.pickle', 'rb'))

@app.route('/predict-price', methods=['POST'])
def predict_price():
    if request.method == 'POST':
        features = []
        data = request.form
        for field in fields:
            if field == 'floor' or field == 'rooms':
                features.append(int(data.get(field)))
            elif field == 'area':
                features.append(float(data.get(field)))
            else:
                features.append(data.get(field))
        final_features = ([features])
        prediction = model.predict(final_features)
    return {
        'predicted_price': str(prediction[0])
    }

if __name__ == '__main__':
    app.run(debug=True)