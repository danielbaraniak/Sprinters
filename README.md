# Sprinters

Competance project

## ML

### Prerequisits

Install all the requirements

```bash
pip3 install -r requirements.txt
```

### Generating models

- [`ML.src.features_info`](ML/src/features_info.py) describes which features are used for training.
- [`ML/settings.cfg`](ML/settings.cfg) contains configuration of the folders and `custom_model`. If `custom_model` is not set, hyperparameters are found from [`ML.src.features_info.hyparam_grid`](ML/src/features_info.py).

Following command generates the model:

```bash
launch.py --train
```

### Using models

`model.predict` expects `pandas.Dataframe` with specific column names for an input. `Dataframe` can be created from dictionary like this:

```python
import joblib
import pandas as pd

request = {
 'offer_type': 'Private',
 'floor': 4.0,
 'area': 67.0,
 'rooms': 4,
 'offer_type_of_building': 'Housing Block',
 'market': 'aftermarket',
 'longitude': 21.549882888793945,
 'latitude': 51.58496856689453,
 'population': 18277.0,
}

loaded_model = joblib.load("../models/2022-11-13 19:09:05.094617.pkl")
single_X = pd.DataFrame({k: [v] for k, v in request.items()})

result = loaded_model.predict(single_X)[0]
```
