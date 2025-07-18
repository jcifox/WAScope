import json
import argparse

import requests
import core.RequestConstructor as ReqConstr
from core.ControllerRequestRecord import ControllerRequestRecord
import lib.Utils as Utility
import core.Analyzer as Analyzer


def init(_host, _method='get', _content_type='json'):
    where_condition = ("host='{host}' and content_type='{content_type}' and method='{method}' and {method}_params!='' "
                       "and response_exists_sensitive>0 ").format(host=_host, content_type=_content_type, method=_method)
    fields = "distinct(url) as url,referer,{method}_params,{method}_sensitive,response".format(method=_method)
    CtrlReqRecd = ControllerRequestRecord()
    rs = CtrlReqRecd.query_record(where=where_condition, fields=fields)
    header = ReqConstr.get_header(_host)
    rs_gen = []
    if _method == 'get':
        for rs_item in rs:
            # print(rs_item)
            rs_gen.append({"origin": rs_item, "gen": ReqConstr.build_url(rs_item["url"], rs_item[_method + "_params"])})
    elif _method == 'post':
        for rs_item in rs:
            # print(rs_item)
            rs_gen.append({"origin": rs_item, "url": rs_item["url"], "gen": ReqConstr.build_params(rs_item[_method + "_params"])})
    return {"header": header, "rs": rs_gen}


def add_record(_data):
    origin_params, sensitive_params = Analyzer.content_analysis(Utility.remove_html_tags(_data["response"]))
    sensitive_params_len = 0
    sensitive_info = ''
    if sensitive_params is not None and len(sensitive_params) > 0:
        sensitive_params_len = len(sensitive_params)
        sensitive_info = json.dumps(sensitive_params, ensure_ascii=False)
    second_record_item = {
        "host": _data['host'], "method": _data['method'], "referer": _data['rs_item']['origin']['referer'],
        "content_type": "json", "origin_url": _data['rs_item']['origin']['url'],
        "url": _data['gen_url'], "response": _data["response"], "response_exists_sensitive": sensitive_params_len,
        "response_sensitive": sensitive_info, "gen_params": _data['gen_params']
    }
    CtrlReqRecd = ControllerRequestRecord()
    CtrlReqRecd.add_request_record_second(second_record_item)


def replay(_host, _method='get'):
    rs = init(_host, _method)
    # print("==========second_request - rs==========")
    # print(rs)
    # print("==========second_request - rs==========")
    header = json.loads(rs["header"])
    # resp = []
    for rs_item in rs["rs"]:
        # tmp_resp = []
        for gen in rs_item["gen"]:
            _data = {
                "host": _host, "method": _method, "rs_item": rs_item
            }
            if _method == 'get':
                t_resp = requests.get(gen, headers=header)
                res_txt = t_resp.text.replace("'", "")
                res_txt = Utility.remove_html_tags(res_txt)
                _data['response'] = res_txt
                _data['gen_url'] = gen
                _data['gen_params'] = gen.split('?')[1]
            elif _method == 'post':
                t_resp = requests.post(rs_item['url'], headers=header, data=gen)
                res_txt = t_resp.text.replace("'", "")
                res_txt = Utility.remove_html_tags(res_txt)
                _data['response'] = res_txt
                _data['gen_url'] = rs_item['url']
                _data['gen_params'] = json.dumps(gen)
            add_record(_data)
            print("【{}】Current URL & Paras：{},{}".format(_method, _data['gen_url'], _data['gen_params']))
    print("【{}】Replay Completed".format(_method))


def replay_post(_host):
    replay(_host, 'post')


def replay_get(_host):
    replay(_host, 'get')


def run(_host):
    replay_get(_host)
    replay_post(_host)

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='')
args = parser.parse_args()
host = args.host
print("host:", host)
run(host)
