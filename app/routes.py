from app import app
from flask import jsonify
from app.controller.bms import BMS
from app.controller.irradiance import Irradiance
from utils import get_three_dates_before


@app.route('/uploadbms/<bss>', methods=['POST'])
def upload_bms(bss):
    try:
        obj_bms = BMS()
        obj_bms.upload_bms()
        result = obj_bms.get_bms(bss)
        response = {"message": "Data berhasil dikirim", "data": result}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Data gagal terkirim", "error": str(e)}
        return jsonify(error_response), 500


@app.route('/getidbms')
def get_id_bms():
    try:
        obj_bms = BMS()
        result = obj_bms.get_id_bms()

        response = {"message": "Sukses", "data": result}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Terjadi kesalahan", "error": str(e)}
        return jsonify(error_response), 500
    

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
    

@app.route('/autouploadbms', methods=['POST'])
def auto_upload_bms():
    try:
        obj_bms = BMS()
        obj_bms.auto_input_bms()

        response = {"message": "Data berhasil dikirim"}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Data gagal terkirim", "error": str(e)}
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
    

@app.route('/autouploadirradiance', methods=['POST'])
def auto_upload_irradiance():
    try:
        obj_irr = Irradiance()
        obj_irr.auto_upload_file()
        response = {"message": "Data berhasil dikirim"}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Data gagal terkirim", "error": str(e)}
        return jsonify(error_response), 500


@app.route('/getirradiance/<tanggal>')
def get_irradiance(tanggal):
    try:
        obj_irr = Irradiance()
        result = obj_irr.get_irradiance(tanggal)
        
        response = {"message": "Sukses", "data": result}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Terjadi kesalahan", "error": str(e)}
        return jsonify(error_response), 500
    

@app.route('/getminirradiance/<tanggal>')
def get_min_irradiance(tanggal):
    try:
        obj_irr = Irradiance()
        result_df = obj_irr.get_min_irradiance(tanggal)
        result_list = result_df.to_dict(orient='records')
        response = {"message": "Sukses", "data":result_list}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Terjadi kesalahan", "error": str(e)}
        return jsonify(error_response), 500
    

@app.route('/getmaxirradiance/<tanggal>')
def get_max_irradiance(tanggal):
    try:
        obj_irr = Irradiance()
        result_df = obj_irr.get_max_irradiance(tanggal)
        result_list = result_df.to_dict(orient='records')
        response = {"message": "Sukses", "data":result_list}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Terjadi kesalahan", "error": str(e)}
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
    

@app.route('/checkbms/<tanggal>')
def check_bms(tanggal):
    try:
        obj_bms = BMS()
        result = obj_bms.check_bms('2024-08-12')
        
        response = {"message": "Sukses", "data": result}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Terjadi kesalahan", "error": str(e)}
        return jsonify(error_response), 500
    


    

