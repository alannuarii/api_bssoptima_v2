import pandas as pd
import pickle

# Inisiasi model 
model_cap_rul = 'app/model/capacity_to_rul/capacity_to_rul.pkl'

def cap_to_rul(input):
    data = {'Capacity': [input]}

    feature = pd.DataFrame(data)

    with open(model_cap_rul, 'rb') as file:
        loaded_model = pickle.load(file)

    rul = loaded_model.predict(feature)

    return rul[0]






