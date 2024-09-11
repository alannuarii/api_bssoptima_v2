from app import app
from flask import jsonify
from app.controller.bms import BMS
from app.controller.irradiance import Irradiance
from utils import get_three_dates_before


@app.route('/getbms/<bss>')
def get_bms(bss):
    try:
        obj_bms = BMS()
        result = obj_bms.get_bms(bss)
        
        response = {"message": "Sukses", "data": result}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Terjadi kesalahan", "error": str(e)}
        return jsonify(error_response), 500
    

@app.route('/uploadirradiance', methods=['POST'])
def upload_irradiance():
    try:
        obj_irr = Irradiance()
        obj_irr.upload_file()
        response = {"message": "Data berhasil dikirim"}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Data gagal terkirim", "error": str(e)}
        return jsonify(error_response), 500
    

@app.route('/optimization/<tanggal>')
def get_optimization(tanggal):
    dates = get_three_dates_before(tanggal)
    try:
        obj_irr = Irradiance()
        datas = []
        for i in range(len(dates)):
            irradiance = obj_irr.get_irradiance(dates[i])
            datas.append(irradiance)
        
        result_df_avg = obj_irr.get_min_irradiance(datas[2], datas[1], datas[0])
        result_df_max = obj_irr.get_max_irradiance(datas[2], datas[1], datas[0])

        result_list_avg = result_df_avg.to_dict(orient='records')
        result_list_max = result_df_max.to_dict(orient='records')
        response = {"message": "Sukses", "data":{
            "irr1":datas[2],
            "irr2":datas[1],
            "irr3":datas[0],
            "avg":result_list_avg,
            "max":result_list_max
        }}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Terjadi kesalahan", "error": str(e), "data":{
            "irr1":[],
            "irr2":[],
            "irr3":[],
            "avg":[],
            "max":[]
        }}
        return jsonify(error_response), 500
    

@app.route('/getlast4days')
def get_last_4days():
    try:
        obj_irr = Irradiance()
        result = obj_irr.get_last_4days()
        
        response = {"message": "Sukses", "data": result}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Terjadi kesalahan", "error": str(e)}
        return jsonify(error_response), 500
    

@app.route('/deletedata', methods=['POST'])
def delete_data():
    try:
        obj_irr = Irradiance()
        obj_irr.delete_oldest_data()
        
        response = {"message": "Sukses hapus data lama"}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Terjadi kesalahan", "error": str(e)}
        return jsonify(error_response), 500

    


    

