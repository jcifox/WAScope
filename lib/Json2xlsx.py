import json
import pandas as pd
import os


# json to xlsx
def file_name(file_path):    
    paths_list = []
    for root, dirs, files in os.walk(file_path):
        for file in files:
            path_list = os.path.join(root, file)
            paths_list.append(path_list)
    return paths_list


def json_out(file_path, xls_path='./'):
    with open(file_path, "r", encoding='utf-8') as f:
        data = json.load(f)
        print(data)
    data = pd.DataFrame(data)
    data.to_excel(xls_path, index=None)


def json_outs(file_path, xls_path='./'):
    path_lists = file_name(file_path)
    list_data = []
    for path in path_lists:
        try:
            with open(path, "r", encoding='utf-8') as f:
                data = json.load(f)
                print(data)
                data = pd.DataFrame(data)
                list_data.append(data)
        except Exception as e:
            print("error:", e)
    total_data = pd.concat(list_data)
    total_data.to_excel(xls_path, index=None)
