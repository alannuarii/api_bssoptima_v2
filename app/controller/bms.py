from db import connection
from flask import request
from datetime import date,timedelta


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
        self.insert_bms(id_bms, tanggal, voltage, temperature)
        self.get_bms()


    def insert_bms(self, id_bms, tanggal, voltage, temperature):
        query = f"INSERT INTO bms (id_bms, tanggal, voltage, temperature) VALUES (%s, %s, %s, %s)"
        value = [id_bms, tanggal, voltage, temperature]
        connection(query, 'insert', value)

    def get_bms(self):
        query = f"SELECT id_bms FROM bms WHERE tanggal >= %s AND tanggal <= %s ORDER BY id_bms"
        value = self.get_week()
        result = connection(query, 'select', value)
        return result