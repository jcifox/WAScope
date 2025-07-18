import itertools
import json
import urllib.parse

import lib.Utils as Utility


def get_header(_host):
    try:
        header_path = './mitmproxy/{host}/header.json'.format(host=_host)
        code = Utility.open_json_file(header_path)
        # print(code)
        header = code['request_header']
    except FileNotFoundError:
        header = None
        print("header.json not found")
    return header

def build_params(_params, start_index=1, end_index=20):
    get_param = json.loads(_params)
    # print(get_param)
    tmp_seq_params = {}
    for params_key in get_param:
        # print(get_param, params_key)
        try:
            # print(get_param[params_key])
            # print(utiles.has_digit(get_param[params_key]))
            if Utility.has_digit(get_param[params_key]):
                # print(get_param[params_key])
                params_gen_val = Utility.generate_sequence(get_param[params_key], start_index, end_index)
                # print(params_gen_val)
                tmp_seq_params[params_key] = []
                # print(params_gen_val)
                for params_key_val in params_gen_val:
                    tmp_seq_params[params_key].append(params_key_val)
            else:
                tmp_seq_params[params_key] = [get_param[params_key]]
        except Exception as e:
            pass
    keys = list(tmp_seq_params.keys())
    combinations = list(itertools.product(*tmp_seq_params.values()))
    tmp_para = []
    for combination in combinations:
        para = {}
        for i in range(len(keys)):
            para[keys[i]] = combination[i]
        tmp_para.append(para)
    return tmp_para


def build_url(_url, _params, start_index=1, end_index=10):
    tmp_url = []
    g_url_root = _url.split('?')[0]
    gen_params = build_params(_params, start_index, end_index)
    for para_item in gen_params:
        tmp_url.append(g_url_root + "?" + urllib.parse.urlencode(para_item))
    return tmp_url