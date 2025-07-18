# -*- coding: utf-8 -*-
# System Lib Dependencies
import json
import os
from requests_html import AsyncHTMLSession
# Custom Dependencies
import core.Analyzer as Analyzer
import core.Config as Config
import core.Filter as Filter
import lib.Utils as Utility
from core.ControllerRequestRecord import ControllerRequestRecord
from mitmproxy import ctx

httpRecord = []
package = ''


def load(loader):
    loader.add_option(name="package", typespec=str, default='no input package', help="app package")


def request(flow):
    global package
    package = ctx.options.package
    # print(package)
    # print("request_flow_id", flow.id)
    request_data = flow.request
    # print("request_data:===>", json.dumps(request_data))
    # print("request_data:===>", request_data.content)
    header = request_data.headers
    global httpRecord
    preHeader = {}
    for f in header.fields:
        # print(f[0].decode(), f[1].decode())
        preHeader[f[0].decode()] = f[1].decode()
    if 'Accept-Encoding' in preHeader:
        preHeader.pop('Accept-Encoding')
    # print("preHeader['Referer']===>>>", preHeader['Referer'])
    referer = preHeader['Referer'] if 'Referer' in preHeader else ''
    preHeader = json.dumps(preHeader)
    req = {
        "flow_id": flow.id,
        "host": str(request_data.host).lower(),
        "method": str(request_data.method).lower(),
        "url": str(request_data.url),
        "referer": str(referer),
        "path": request_data.path,
        "port": str(request_data.port),
        "cookies": str(request_data.cookies),
        'request_header': preHeader
    }

    get_sensitive = {}
    get_params = {}

    post_sensitive = {}
    post_params = {}

    path_params, path_sensitive = Analyzer.path_analysis(req['path'])
    req['path_sensitive'] = json.dumps(path_sensitive) if len(path_sensitive) > 0 else ''
    req['path_exist_sensitive'] = len(path_sensitive)
    check_had_get_params = Filter.check_question_mark(req['path'])
    if check_had_get_params:
        get_params, get_sensitive = Analyzer.params_analysis(req['url'])
        print("get--get_params====>", get_params)
        print("get--sensitive_params====>", get_sensitive)
    if req['method'] == 'post':
        if "Content-Type" in header:
            ct_flag = False
            for ct in Config.post_content_type:
                if ct in header['Content-Type']:
                    ct_flag = True
                    break
            if ct_flag:
                if header['Content-Type'] == 'application/json':
                    post_params, post_sensitive = Analyzer.params_analysis(request_data.content.decode('utf-8'), True)
                else:
                    post_params, post_sensitive = Analyzer.params_analysis(request_data.get_text())
                print("post--origin_params====>", post_params)
                print("post--sensitive_params====>", post_sensitive)

    req['get_params'] = json.dumps(get_params) if len(get_params) > 0 else ''
    req['get_exist_sensitive'] = len(get_sensitive)
    req['get_sensitive'] = json.dumps(get_sensitive) if len(get_sensitive) > 0 else ''

    print("========post_params========")
    print(post_params)
    print("========post_params========")

    req['post_params'] = json.dumps(post_params) if len(post_params) > 0 else ''
    req['post_exist_sensitive'] = len(post_sensitive)
    req['post_sensitive'] = json.dumps(post_sensitive) if len(post_sensitive) > 0 else ''

    # check host
    host_flag = Filter.check_host(req['host'])
    print("host:", req['host'])
    # check method
    method_flag = Filter.check_method(req['method'])
    print("host_flag===>", host_flag)
    print("method_flag===>", method_flag)
    if host_flag and method_flag:
        httpRecord.append(req)
        save_host_header(req)


def response(flow):
    resp = flow.response
    header = resp.headers
    global httpRecord
    preHeader = {}

    # print("\n========[" + flow.id + "]response header START========\n")
    for f in header.fields:
        # print(f[0].decode(), f[1].decode())
        preHeader[f[0].decode()] = f[1].decode()
    # print("\n========[" + flow.id + "]response header END========\n")
    # print(type(response.text))
    # print("\n========\n")
    contentType = preHeader['Content-Type'] if 'Content-Type' in preHeader else ''
    content_type_flag = False
    if len(resp.text) > 10:
        if Filter.check_is_json(resp.text):
            content_type_flag = True
            contentType = 'json'

        if Filter.check_is_html(contentType):
            content_type_flag = True
            contentType = 'html'

    ctrlRequestRecord = ControllerRequestRecord()

    if content_type_flag:
        # global httpRecord
        for record_item in httpRecord:
            if record_item['flow_id'] == flow.id:
                res_txt = resp.text.replace("'", "")
                res_txt = Utility.remove_html_tags(res_txt)
                record_item['response'] = res_txt
                origin_params, sensitive_params = Analyzer.content_analysis(res_txt)
                sensitive_params_len = 0
                sensitive_info = ''
                if sensitive_params is not None and len(sensitive_params) > 0:
                    sensitive_params_len = len(sensitive_params)
                    sensitive_info = json.dumps(sensitive_params, ensure_ascii=False)
                    print("====Response seneitive：{0}====".format(sensitive_params_len))
                    print(sensitive_info)
                    print("====Response seneitive：End====")
                record_item['response_exists_sensitive'] = sensitive_params_len
                record_item['response_sensitive'] = sensitive_info
                record_item['content_type'] = contentType
                ctrlRequestRecord.add_record(record_item)

    else:
        print("response invalid")


def save_host_header(_data):
    dir_path = "./mitmproxy/" + _data['host'] + "/"
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)

    w_data = {
        "request_header": _data['request_header'],
        "cookie": _data['cookies']
    }

    file_path = dir_path + "header.json"
    with open(file_path, mode='w', encoding="utf-8") as json_file:
        json.dump(w_data, json_file, ensure_ascii=False)
