from db import connection
from flask import request
from datetime import date,timedelta, datetime
from app.model.voltage_to_capacity.predict_capacity import vol_to_cap
from app.model.capacity_to_rul.predict_rul import cap_to_rul
import random


class BMS:
    def get_week(self):
        today = date.today()
        if today.weekday() == 4:
            last_friday = today
        else:
            days_to_last_friday = (today.weekday() - 4) % 7
            last_friday = today - timedelta(days=days_to_last_friday)

        days_to_next_thursday = (3 - today.weekday() + 7) % 7
        next_thursday = today + timedelta(days=days_to_next_thursday)

        return [last_friday, next_thursday]

    def upload_bms(self):
        id_bms = request.form['id_bms']
        tanggal = request.form['tanggal']
        voltage = request.form['voltage']
        temperature = request.form['temperature']
        capacity = vol_to_cap(voltage)
        rul = cap_to_rul(capacity)
        self.insert_bms(id_bms, tanggal, voltage, temperature, capacity, rul)
        self.get_id_bms()

    def insert_bms(self, id_bms, tanggal, voltage, temperature, capacity, rul):
        query = f"INSERT INTO bms (id_bms, tanggal, voltage, temperature, capacity, rul) VALUES (%s, %s, %s, %s, %s, %s)"
        value = [id_bms, tanggal, voltage, temperature, capacity, rul]
        connection(query, 'insert', value)

    def get_id_bms(self):
        query = f"SELECT id_bms FROM bms WHERE tanggal >= %s AND tanggal <= %s ORDER BY id_bms"
        value = self.get_week()
        result = connection(query, 'select', value)
        return result
    
    def get_bms(self, bss):
        if bss == 'bss1':
            query = f"SELECT * FROM bms WHERE tanggal >= %s AND tanggal <= %s AND id_bms < 89 ORDER BY id_bms"
            value = self.get_week()
            result = connection(query, 'select', value)
            return result
        elif bss == 'bss2':
            query = f"SELECT * FROM bms WHERE tanggal >= %s AND tanggal <= %s AND id_bms > 88 ORDER BY id_bms"
            value = self.get_week()
            result = connection(query, 'select', value)
            return result
    
    def auto_input_bms(self):
        today = datetime.now()
        tanggal = today.strftime("%Y-%m-%d")
        number_day = today.weekday()
        if number_day == 4 and self.check_bms(tanggal) == []:
            for i in range(176):
                volt_random = round(random.uniform(50,55), 2)
                temp_random = round(random.uniform(17,25), 2)
                capacity = vol_to_cap(volt_random)
                rul = cap_to_rul(capacity)
                self.insert_bms(i+1, tanggal, volt_random, temp_random, capacity, rul)
            print('Input Data Berhasil')
        else:
            print(f"Data pada tanggal {tanggal} sudah ada")


    def check_bms(self, tanggal):
        query = f"SELECT * FROM bms WHERE tanggal = %s"
        value = [tanggal]
        result = connection(query, 'select', value)
        return result