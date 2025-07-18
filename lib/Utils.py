import hashlib
import json
import re
from bs4 import BeautifulSoup


def pattern_handler(_params):
    return r'\b({0})\b'.format("|".join(_params))


def pay_load_json_handler(_json_str):
    parsed_list = []
    try:
        json_data = json.loads(_json_str)
        if isinstance(json_data, dict):
            parsed_list = list(json_data.items())
        else:
            print("json_str not object")
    except json.JSONDecodeError:
        print("json_str illegal")
    return parsed_list

def json2dict(_str):
    return json.loads(_str)


def dict2json(_dict, _ensure_ascii=False):
    return json.dumps(_dict, ensure_ascii=_ensure_ascii)


def md5(_str):
    _md5 = hashlib.md5()
    _md5.update(_str.encode('utf-8'))
    return _md5.hexdigest()


def open_json_file(_path):
    with open(_path, 'r') as f:
        data = json.load(f)
    return data


def check_zero_prefix(_str):
    count = 0
    for i in range(len(_str)):
        if _str[i] == '0':
            count += 1
        else:
            break
    return count


def generate_sequence(_str, start, end):
    _str = str(_str)
    zero_prefix_count = check_zero_prefix(_str)
    sequence = []
    if _str.isnumeric():
        number = int(_str)
        suffix = ''
        sequence.append(int(_str))
    else:
        pattern = r'(\d*)(\D*)(\d*)$'
        match = re.search(pattern, _str)
        if match is None:
            return []
        suffix = match.group(1) + "" + match.group(2)
        number = int(match.group(3))
        sequence.append(_str)
    for i in range(start, end):
        if number - i > 0:
            new_string = f"{suffix}{number - i}"
            sequence.append(new_string)
    for i in range(start, end + 1):
        new_string = f"{suffix}{number + i}"
        sequence.append(new_string)
    if zero_prefix_count > 0:
        for i, v in enumerate(sequence):
            for z in range(zero_prefix_count):
                sequence[i] = "0" + str(sequence[i])
    # print(sequence)
    return sequence


def has_digit(_str):
    string = str(_str)
    try:
        for char in string:
            if char.isdigit():
                return True
    except Exception as e:
        return False
    pass


def remove_html_tags(_str):
    soup = BeautifulSoup(_str, 'html.parser')
    txt = soup.get_text()
    txt = txt.replace('\xa0', '')
    txt = txt.replace(' ', '')
    return txt


def is_hash_exists(hash_value, array, fields):
    for element in array:
        # print(element[fields], hash_value)
        if element[fields] == hash_value:
            return True
    return False


def build_tree(data):
    result = {}
    for item in data:
        method = item['method']
        gen_params = item['gen_params']
        referer = item['referer']
        origin_url = item['origin_url']
        url = item['url']
        response_hash = item['response_hash']
        # response = item['response']
        response_sensitive = item['response_sensitive']
        response_exists_sensitive = item['response_exists_sensitive']

        if referer not in result:
            result[referer] = []

        gen_data = {
            "url": url, "response_hash": response_hash,
            "gen_params": gen_params,
            "sensitives_nums": response_exists_sensitive,
            "response_sensitive": response_sensitive
        }
        # gen_data = {"gen_url": gen_url, "response_hash": response_hash}
        # Check if the origin_url already exists in the result
        flag = False
        for url_data in result[referer]:
            if url_data['api'] == origin_url:
                # print(is_hash_exists(gen_data['response_hash'], url_data['gen'], 'response_hash'))
                if not is_hash_exists(gen_data['response_hash'], url_data['gen'], 'response_hash'):
                    url_data['gen'].append(gen_data)
                    url_data['taint_analysis'].append({
                        "source": gen_data['response_sensitive'],
                        "sink": gen_data['url'],
                        "path": referer,
                        "gen_params": gen_data['gen_params'],
                        "source_sensitives_nums": gen_data['sensitives_nums']
                    })
                    flag = True
                break

        if not flag:
            result[referer].append({"api": origin_url, "method": method, "gen": [gen_data], "taint_analysis": []})

    return [{"referer": referer, "page": urls} for referer, urls in result.items()]


def handler_source(_source, limit=50):
    _source = _source.replace('\xa0', '')
    _source = _source.replace(' ', '')
    try:
        _source = json.loads(_source)
        for key, value in _source.items():
            if isinstance(value, str) and len(value) > 50:
                _source[key] = value[:50]  
        return str(_source)
    except json.decoder.JSONDecodeError as e:
        return "None"
        pass


def disable_sign_escape(_text, _sign="&", _re_txt="&amp;"):
    return _text.replace(_sign, _re_txt)
