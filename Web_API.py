import os
import base64
from flask import Flask, jsonify, send_from_directory, render_template
from flask_cors import CORS
from core.ControllerRequestRecord import ControllerRequestRecord
from core.ReportGenerator import create_report

app = Flask(__name__)
app.template_folder = 'report_output'  # defined report output dir
# CORS
CORS(app, resources=r'/*')


def default_respond():
    return 2000, "success", []


def respond(_data=None, _msg="success", _code=2000):
    _data = {} if _data is None else _data
    return jsonify({
        "code": _code,
        "msg": _msg,
        "data": _data
    })


@app.route('/')
def home():
    return "Access Denied"


# set icon
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


# get hosts list
@app.route('/hosts_list')
def hosts_list():
    CtrlReqRecd = ControllerRequestRecord()
    rs = CtrlReqRecd.query_record_second(fields='distinct(host),to_base64(host) as host_base64', where='1=1 order by create_time desc ')
    return respond(_data=rs)


# get host analysis result
@app.route('/analysis/<_host>')
def analysis(_host):
    code, msg, data = default_respond()
    report = ''
    try:
        host = base64.urlsafe_b64decode(_host).decode('utf-8')
        CtrlReqRecd = ControllerRequestRecord()
        data = CtrlReqRecd.query_record_second_analysis(_host=host)
        report = create_report(_host=host)
    except Exception as e:
        print(str(e))
        msg = 'params host illegal'
        code = 4000
    return respond(_data={"list": data, "report": report}, _msg=msg, _code=code)


@app.route('/analysis_report/<_file>')
def analysis_report(_file):
    code, msg, data = default_respond()
    try:
        file = base64.urlsafe_b64decode(_file).decode('utf-8')
        return render_template(file)
    except Exception as e:
        msg = str(e)
        code = 4000
        return respond(_data=data, _msg=msg, _code=code)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=1001, debug=False)
