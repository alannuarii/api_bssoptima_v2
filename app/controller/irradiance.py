from flask import request
from db import connection
from db2 import df_to_sql
from datetime import datetime, timedelta
from utils import get_three_dates_before
from math import isnan
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
    

    def get_rekap_data(self, bulan):
        query = f"SELECT * FROM setting_parameter WHERE DATE_FORMAT(tanggal, '%Y-%m') = %s"
        value = [bulan]
        result = connection(query, "select", value)
        return result
    
    def get_setting_parameter(self):
        today = datetime.today().strftime('%Y-%m-%d')
        query = f"SELECT * FROM setting_parameter WHERE tanggal = %s"
        value = [today]
        result = connection(query, 'select', value)
        return result
    
    def post_setting_parameter(self):
        today = datetime.today().strftime('%Y-%m-%d')
        dates = get_three_dates_before(today)

        datas = []
        for i in range(len(dates)):
            irradiance = self.get_irradiance(dates[i])
            datas.append(irradiance)
        
        # Mengambil irradiance minimum dan maksimum
        result_df_avg = self.get_min_irradiance(datas[2], datas[1], datas[0])
        result_df_max = self.get_max_irradiance(datas[2], datas[1], datas[0])

        # Mengubah dataframe menjadi list of dictionaries
        result_list_avg = result_df_avg.to_dict(orient='records')
        result_list_max = result_df_max.to_dict(orient='records')

        # Jika data avg dan max tersedia, ambil irradiance
        minIrr = result_list_avg if len(result_list_avg) > 0 else []
        maxIrr = result_list_max if len(result_list_max) > 0 else []

        # Menghitung y4 dan y5
        y4 = [item['irradiance'] for item in minIrr]
        sumMin = [item['irradiance'] / 360 for item in minIrr]
        totalMin = sum(sumMin)
        forecastProduksiPV = totalMin * 6.8 * 0.1917

        y5 = [item['irradiance'] for item in maxIrr]
        sumMax = [item['irradiance'] / 360 for item in maxIrr]
        totalMax = sum(sumMax)
        forecastProduksiPVBSS = totalMax * 6.8 * 0.1917

        # Menghitung arrayRampRate
        arrayRampRate = []
        for i in range(1, len(y4)):
            if i < len(y5):  # Pastikan indeks y5 valid
                selisih = y5[i] - y4[i-1]
                if not isnan(selisih):
                    arrayRampRate.append(selisih)

        # Menghitung arrayMaxBeban
        arrayMaxBeban = []
        for i in range(1, len(y4)):
            selisih = y5[i] - y4[i-1] if i < len(y5) else float('nan')
            arrayMaxBeban.append(selisih)

        # Menghitung forecastSmooting, kebutuhanDoD, maxBebanBSS, dan rampRate
        forecastSmooting = forecastProduksiPVBSS - forecastProduksiPV
        kebutuhanDoD = (forecastSmooting / 900) * 100
        maxBebanBSS = min(max(arrayMaxBeban) * 6.8 * 0.1917, 600)
        rampRate = min(max(arrayRampRate) * 6.8 * 0.1917, 20)
        crate = 0.2

        data = self.get_setting_parameter()

        if not data:
            query = f"INSERT INTO setting_parameter (tanggal, dod, crate, ramprate, maxbss, prod_pv, smooth_bss, total_pv_bss) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
            value = [today, kebutuhanDoD, crate, rampRate, maxBebanBSS, forecastProduksiPV, forecastSmooting, forecastProduksiPVBSS]
            connection(query, 'insert', value)
        else:
            query = f"UPDATE setting_parameter SET dod = %s, crate = %s, ramprate = %s, maxbss = %s, prod_pv = %s, smooth_bss = %s, total_pv_bss = %s WHERE id = %s"
            value = [kebutuhanDoD, crate, rampRate, maxBebanBSS, forecastProduksiPV, forecastSmooting, forecastProduksiPVBSS, data[0]['id']]
            connection(query, 'update', value)