from datetime import datetime, timedelta

def get_three_dates_before(input_date):
    # Konversi tanggal input menjadi objek datetime
    input_datetime = datetime.strptime(input_date, '%Y-%m-%d')

    # Inisialisasi list untuk menyimpan tanggal
    dates_list = []

    # Tambahkan tanggal input ke dalam list
    dates_list.append(input_date)

    # Kurangkan 1 hari dari tanggal input dan tambahkan ke dalam list
    one_day_before = input_datetime - timedelta(days=1)
    dates_list.append(one_day_before.strftime('%Y-%m-%d'))

    # Kurangkan 2 hari dari tanggal input dan tambahkan ke dalam list
    two_days_before = input_datetime - timedelta(days=2)
    dates_list.append(two_days_before.strftime('%Y-%m-%d'))

    return dates_list