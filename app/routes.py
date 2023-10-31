from app import app
from flask import jsonify, request
from app.controller.bms import BMS


@app.route('/uploadbms', methods=['GET', 'POST'])
def upload_bms():
    if request.method == 'POST':
        try:
            obj_bms = BMS()
            obj_bms.upload_bms()
            result = obj_bms.get_bms()

        except Exception as e:
            error_response = {"message": "Data gagal terkirim", "error": str(e)}
            return jsonify(error_response), 500

    response = {"message": "Data berhasil dikirim", "data": result}
    return jsonify(response), 200


@app.route('/getbms')
def get_bms():
    try:
        obj_bms = BMS()
        result = obj_bms.get_bms()

        response = {"message": "Sukses", "data": result}
        return jsonify(response), 200

    except Exception as e:
        error_response = {"message": "Terjadi kesalahan", "error": str(e)}
        return jsonify(error_response), 500