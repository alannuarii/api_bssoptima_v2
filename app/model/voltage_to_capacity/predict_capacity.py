import pandas as pd
import pickle

# Inisiasi model 
model_volt_cap = 'app/model/voltage_to_capacity/voltage_to_capacity.pkl'

def vol_to_cap(input):
    data = {'Voltage': [input]}

    feature = pd.DataFrame(data)

    with open(model_volt_cap, 'rb') as file:
        loaded_model = pickle.load(file)

    capacity = loaded_model.predict(feature)

    return capacity[0]



