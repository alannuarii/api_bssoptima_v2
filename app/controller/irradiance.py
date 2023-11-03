from flask import request
from db import connection
from db2 import df_to_sql
import pandas as pd
from datetime import datetime, timedelta


class Irradiance:
    def upload_file(self):
        file = request.files['irradiance']
        df = pd.read_csv(file)
        df.drop(df.columns[[1,2,4,5,6,7,8,9,10,11,12,13,14,15,16]], axis=1, inplace=True)
        df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %H:%M:%S')
        df['Time'] = df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.rename(columns={'Time': 'waktu', 'Global Irradiance': 'irradiance'}, inplace=True)
        df_to_sql(df, 'irradiance')


    def insert_irradiance(self, waktu, irradiance):
        query = f"INSERT INTO irradiance (waktu, irradiance) VALUES (%s, %s)"
        value = [waktu, irradiance]
        connection(query, 'insert', value)


    def get_irradiance(self, tanggal):
        query = f"SELECT * FROM irradiance WHERE DATE(waktu) = %s ORDER BY waktu"
        value = [tanggal]
        result = connection(query, 'select', value)
        return result


    # def upload_file(self):
    #     file = request.files['irradiance']
    #     df = pd.read_csv(file)
    #     df.drop(df.columns[[1,2,4,5,6,7,8,9,10,11,12,13,14,15,16]], axis=1, inplace=True)
    #     df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %H:%M:%S')
    #     df_grouped = df.groupby(df['Time'].dt.strftime('%m/%d/%Y %H:%M'))
    #     df_averaged = df_grouped['Global Irradiance'].mean().reset_index()
    #     df_averaged['Time'] = pd.to_datetime(df_averaged['Time'], format='%m/%d/%Y %H:%M')
    #     df_averaged['Time'] = df_averaged['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
    #     df_averaged.rename(columns={'Time': 'waktu', 'Global Irradiance': 'irradiance'}, inplace=True)
    #     df_to_sql(df_averaged, 'irradiance')