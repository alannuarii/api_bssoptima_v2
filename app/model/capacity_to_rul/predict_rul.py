import pandas as pd
from joblib import load

# Inisiasi model 
model_cap_rul = 'app/model/capacity_to_rul/capacity_to_rul.pkl'

def cap_to_rul(input):
    data = {'Capacity': [input]}

    feature = pd.DataFrame(data)

    loaded_model = load(model_cap_rul)

    rul = loaded_model.predict(feature)

    return rul[0]






