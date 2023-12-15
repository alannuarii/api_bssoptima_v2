import pandas as pd
from joblib import load

# Inisiasi model 
model_volt_cap = 'app/model/voltage_to_capacity/voltage_to_capacity.pkl'

def vol_to_cap(input):
    data = {'Voltage': [input]}

    feature = pd.DataFrame(data)

    loaded_model = load(model_volt_cap)

    capacity = loaded_model.predict(feature)

    return capacity[0]



