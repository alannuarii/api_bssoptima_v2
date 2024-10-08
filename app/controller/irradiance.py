from flask import request
from db import connection
from db2 import df_to_sql
from datetime import datetime, timedelta
import pandas as pd


class Irradiance:
    def upload_file(self):
        file = request.files['irradiance']
        df = pd.read_csv(file)
        df.drop(df.columns[[1,2,4,5,6,7,8,9,10,11,12,13,14,15,16]], axis=1, inplace=True)
        df['Time'] = pd.to_datetime(df['Time'], format='%m/%d/%Y %H:%M:%S')
        df['Time'] = df['Time'].dt.strftime('%Y-%m-%d %H:%M:%S')
        df.rename(columns={'Time': 'waktu', 'Global Irradiance': 'irradiance'}, inplace=True)
        tanggal = df['waktu'][0][:10]
        if self.check_date_irradiance(tanggal):
            self.delete_irradiance(tanggal)
        df_to_sql(df, 'irradiance')


    def insert_irradiance(self, waktu, irradiance):
        query = f"INSERT INTO irradiance (waktu, irradiance) VALUES (%s, %s)"
        value = [waktu, irradiance]
        connection(query, 'insert', value)


    def get_irradiance(self, tanggal):
        query = f"SELECT waktu, AVG(bssopt.irradiance.irradiance) AS irradiance FROM irradiance WHERE DATE(waktu) = %s GROUP BY waktu ORDER BY waktu"
        value = [tanggal]
        result = connection(query, 'select', value)
        return result
    

    def check_date_irradiance(self, tanggal):
        query = f"SELECT DATE_FORMAT(waktu, '%Y-%m-%d') AS tanggal FROM irradiance WHERE DATE(waktu) = %s LIMIT 1"
        value = [tanggal]
        result = connection(query, 'select', value)
        return result
    

    def delete_irradiance(self, tanggal):
        query = f"DELETE FROM irradiance WHERE DATE(waktu) = %s"
        value = [tanggal]
        connection(query, 'delete', value)

    
    def get_combined_irradiance(self, data1, data2, data3):
        # Filter data to only include non-empty datasets
        datas = [data for data in [data1, data2, data3] if len(data) > 0]

        # If no data is available, return an empty dataframe
        if len(datas) == 0:
            return pd.DataFrame(columns=['waktu', 'irradiance'])

        frames = []
        for data in datas:
            df = pd.DataFrame(data)
            df['waktu'] = pd.to_datetime(df['waktu'], format='%Y-%m-%d %H:%M:%S')
            df['waktu'] = df['waktu'].dt.strftime('%H:%M:%S')
            frames.append(df)

        # Concatenate the valid dataframes and calculate the mean of 'irradiance' grouped by 'waktu'
        combine_df = pd.concat(frames)
        combined_df = combine_df.groupby(['waktu'])['irradiance'].mean().reset_index()

        return combined_df


    def get_min_irradiance(self, data1, data2, data3):
        # Get combined irradiance and find the minimum irradiance grouped by 10-second intervals
        combined_df = self.get_combined_irradiance(data1, data2, data3)
        if combined_df.empty:
            return combined_df

        combined_df['waktu'] = pd.to_datetime(combined_df['waktu'], format='%H:%M:%S')
        min_df = combined_df.groupby(pd.Grouper(key='waktu', freq='10s')).agg({'irradiance': 'min'}).reset_index()

        return min_df
    

    def get_max_irradiance(self, data1, data2, data3):
        # Get combined irradiance and find the maximum irradiance grouped by 10-second intervals
        combined_df = self.get_combined_irradiance(data1, data2, data3)
        if combined_df.empty:
            return combined_df

        combined_df['waktu'] = pd.to_datetime(combined_df['waktu'], format='%H:%M:%S')
        max_df = combined_df.groupby(pd.Grouper(key='waktu', freq='10s')).agg({'irradiance': 'max'}).reset_index()

        return max_df


    def get_last_4days(self):
        query = f"SELECT CAST(waktu AS DATE) AS tanggal FROM irradiance WHERE waktu >= CURDATE() - INTERVAL 4 DAY GROUP BY tanggal"
        value = []
        result = connection(query, 'select', value)
        return result
    

    def delete_oldest_data(self):
        today = datetime.now() + timedelta(hours=8)
        oldest_day = today - timedelta(days=14)
        oldest = oldest_day.replace(hour=6, minute=0, second=0, microsecond=0)

        query = f"DELETE FROM irradiance WHERE waktu < %s"
        value = [oldest]
        connection(query, 'delete', value)


    def get_last_irradiance(self):
        query = f"SELECT waktu FROM irradiance ORDER BY waktu DESC LIMIT %s"
        value = [1]
        result = connection(query, 'select', value)
        return result