from flask import request
from db import connection
from db2 import df_to_sql
import pandas as pd
from utils import get_three_dates_before


class Irradiance:
    def upload_file(self):
        file = request.files['irradiance']
        df = pd.read_csv(file)
        df.drop(df.columns[[1,2,4,5,6,7,8,9,10,11,12,13,14,15,16]], axis=1, inplace=True)
        df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %H:%M:%S')
        df['Time'] = df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.rename(columns={'Time': 'waktu', 'Global Irradiance': 'irradiance'}, inplace=True)
        df_to_sql(df, 'irradiance')
        pd.read_sql


    def insert_irradiance(self, waktu, irradiance):
        query = f"INSERT INTO irradiance (waktu, irradiance) VALUES (%s, %s)"
        value = [waktu, irradiance]
        connection(query, 'insert', value)


    def get_irradiance(self, tanggal):
        query = f"SELECT waktu, irradiance FROM irradiance WHERE DATE(waktu) = %s ORDER BY waktu"
        value = [tanggal]
        result = connection(query, 'select', value)
        return result
    

    def get_combined_irradiance(self, tanggal):
        dates = get_three_dates_before(tanggal)
        data1 = self.get_irradiance(dates[2])
        data2 = self.get_irradiance(dates[1])
        data3 = self.get_irradiance(dates[0])

        df1 = pd.DataFrame(data1)
        df2 = pd.DataFrame(data2)
        df3 = pd.DataFrame(data3)

        df1['waktu'] = pd.to_datetime(df1['waktu'], format='%Y-%m-%d %H:%M:%S')
        df2['waktu'] = pd.to_datetime(df2['waktu'], format='%Y-%m-%d %H:%M:%S')
        df3['waktu'] = pd.to_datetime(df3['waktu'], format='%Y-%m-%d %H:%M:%S')

        df1['waktu'] = df1['waktu'].dt.strftime('%H:%M:%S')
        df2['waktu'] = df2['waktu'].dt.strftime('%H:%M:%S')
        df3['waktu'] = df3['waktu'].dt.strftime('%H:%M:%S')

        frames = [df1, df2, df3]
        combine_df = pd.concat(frames)
        combined_df = combine_df.groupby(['waktu'])['irradiance'].mean().reset_index()

        return combined_df


    def get_averaged_irradiance(self, tanggal):
        combined_df = self.get_combined_irradiance(tanggal)
        combined_df['waktu'] = pd.to_datetime(combined_df['waktu'], format='%H:%M:%S')
        averaged_df = combined_df.groupby(pd.Grouper(key='waktu', freq='10S')).agg({'irradiance': 'mean'}).reset_index()

        return averaged_df
    

    def get_max_irradiance(self, tanggal):
        combined_df = self.get_combined_irradiance(tanggal)
        combined_df['waktu'] = pd.to_datetime(combined_df['waktu'], format='%H:%M:%S')
        max_df = combined_df.groupby(pd.Grouper(key='waktu', freq='10S')).agg({'irradiance': 'max'}).reset_index()

        return max_df