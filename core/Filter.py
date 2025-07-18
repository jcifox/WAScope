import json
import core.Config as Config


def check_empty_collection(_collection):
    return '' if len(_collection) == 0 else _collection


def check_host(_host):
    _host = str(_host).lower()
    flag = False
    for host in Config.hosts:
        if host in _host:
            flag = True
            break
    return flag


def check_method(_method):
    return str(_method).lower() in Config.methods


def check_accept(_accept):
    _accept = str(_accept).lower()
    flag = False
    for t_a in Config.accepts:
        if t_a in _accept:
            flag = True
            break
    return flag


def check_response_content_type(_content_type):
    _content_type = str(_content_type).lower()
    flag = False
    for t_a in Config.response_type:
        if t_a in _content_type:
            flag = True
            break
    return flag


def check_question_mark(_path):
    return "?" in _path


def check_is_json(_str):
    try:
        json.loads(_str)
        return True if _str.replace(" ", "") != "[]" and _str.replace(" ", "") != "{}" else False
    except ValueError:
        return False


def check_is_html(_str):
    return 'text/html' in _str