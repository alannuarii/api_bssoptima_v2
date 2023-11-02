from flask import request
from db import connection
import pandas as pd


class Irradiance:
    def upload_file(self):
        file = request.files['irradiance']
        df = pd.read_csv(file)
        df.drop(df.columns[[1,2,4,5,6,7,8,9,10,11,12,13,14,15,16]], axis=1, inplace=True)
        df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %H:%M:%S')
        df_grouped = df.groupby(df['Time'].dt.strftime('%m/%d/%Y %H:%M'))
        df_averaged = df_grouped['Global Irradiance'].mean().reset_index()
        df_averaged['Time'] = pd.to_datetime(df_averaged['Time'], format='%m/%d/%Y %H:%M')
        df_averaged['Time'] = df_averaged['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        for i in range(len(df_averaged)):
            self.insert_irradiance(df_averaged['Time'][i], df_averaged['Global Irradiance'][i])

    def insert_irradiance(self, waktu, irradiance):
        query = f"INSERT INTO irradiance (waktu, irradiance) VALUES (%s, %s)"
        value = [waktu, irradiance]
        connection(query, 'insert', value)

    def get_irradiance(self, tanggal):
        query = f"SELECT * FROM irradiance WHERE DATE(waktu) = %s ORDER BY waktu"
        value = [tanggal]
        result = connection(query, 'select', value)
        return result
        