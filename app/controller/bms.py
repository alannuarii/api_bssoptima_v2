from db import connection

class BMS:

    def get_bms(self, bss):
        if bss == 'bss1':
            query = f"SELECT b.* FROM battery AS b INNER JOIN (SELECT id_bms, MAX(waktu) AS latest_waktu FROM battery WHERE id_bms < 89 GROUP BY id_bms) AS latest ON b.id_bms = latest.id_bms AND b.waktu = latest.latest_waktu ORDER BY b.id_bms ASC"
            value = []
            result = connection(query, 'select', value)
            return result
        elif bss == 'bss2':
            query = f"SELECT b.* FROM battery AS b INNER JOIN (SELECT id_bms, MAX(waktu) AS latest_waktu FROM battery WHERE id_bms > 88 GROUP BY id_bms) AS latest ON b.id_bms = latest.id_bms AND b.waktu = latest.latest_waktu ORDER BY b.id_bms ASC"
            value = []
            result = connection(query, 'select', value)
            return result   
    