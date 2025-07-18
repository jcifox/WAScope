import os
import time

from lib.DB import DB
from lib import Utils as Utility


class ControllerRequestRecord:
    # init
    db = DB()
    timestamp = str(int(time.mktime(time.localtime(time.time()))))

    def query_record_fusion(self, _host, _content_type='json', _method='get'):
        sql = ("select distinct(a.url) as origin_url,a.referer,b.url as gen_url,b.response_hash,b.response"
               " from request_record a left join request_record_second as b on a.url=b.origin_url"
               " where a.host='{host}' and a.content_type='{content_type}' and a.method='{method}'"
               " and a.get_sensitive!='' and  b.url!='' and b.response not in('[]','')").format(host=_host, content_type=_content_type,
                                                                                                method=_method)
        # print(sql)
        return self.db.query(sql)

    def query_record_second_analysis(self, _host):
        sql = ("select host,method,origin_url,referer,url,gen_params,response_hash,"
               "response_sensitive,response_exists_sensitive,response from request_record_second "
               "group by response_hash HAVING response_exists_sensitive>0 and "
               "host like '%{host}%' order by referer desc,origin_url desc ,url desc").format(host=_host)
        rs = self.db.query(sql)
        return Utility.build_tree(rs)

    def query_record_second(self, where='1=1', fields="*"):
        return self.db.query_request_record_second(where=where, fields=fields)

    def add_request_record_second(self, _data):
        # API Fingerprint
        hash_val = Utility.md5(_data['method'] + _data['gen_params'] + _data['response'])
        add_data_str = ("'{host}','{hash}','{method}','{content_type}',"
                        "'{referer}','{origin_url}',"
                        "'{url}','{response}','{response_exists_sensitive}',"
                        "'{response_sensitive}','{response_hash}','{gen_params}','{timestamp}'")
        add_data = add_data_str.format(host=_data['host'], hash=hash_val, method=_data['method'], content_type=_data['content_type'],
                                       referer=_data['referer'], origin_url=_data['origin_url'],
                                       url=_data['url'], response=_data['response'],
                                       response_exists_sensitive=_data['response_exists_sensitive'],
                                       response_sensitive=_data['response_sensitive'],
                                       response_hash=Utility.md5(_data['response']), gen_params=_data['gen_params'],
                                       timestamp=self.timestamp)
        record_check = self.query_record_second(where="hash='{hash_val}'".format(hash_val=hash_val), fields='id')
        print("record_check===>", len(record_check))
        if len(record_check) == 0:
            # print(add_data_str)
            try:
                self.db.add_request_record_second(values=add_data)
            except Exception as e:
                print("Exception:", str(e))
                dir_path = "./mitmproxy/" + _data['host'] + "/error/"
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                path = _data['url'].split("/")[-1]
                path = path.split("?")[0]
                path = path.replace(".", "_")
                file_path = dir_path + path + "_error.txt"
                w_data = {
                    "exception:": str(e),
                    "url": _data['url'],
                    "data_str": add_data_str,
                    "create_time": self.timestamp
                }
                with open(file_path, mode='a+', encoding="utf-8") as f:
                    f.write(Utility.dict2json(w_data))

    def query_record(self, where, fields="*"):
        return self.db.query_request_record(where=where, fields=fields)

    def add_record(self, _data):
        # API Fingerprint
        hash_val = Utility.md5(_data['method'] + _data['url'] + _data['response'])
        add_data_str = ("'{flow_id}','{host}','{port}','{hash_val}',"
                        "'{method}','{url}','{referer}',"
                        "'{content_type}','{response}','{response_exists_sensitive}',"
                        "'{response_sensitive}',"
                        "'{path}','{path_exist_sensitive}','{path_sensitive}',"
                        "'{get_params}','{get_exist_sensitive}','{get_sensitive}',"
                        "'{post_params}','{post_exist_sensitive}','{post_sensitive}',"
                        "'{timestamp}'")
        add_data = add_data_str.format(
            flow_id=_data['flow_id'], host=_data['host'], port=_data['port'], hash_val=hash_val,
            method=_data['method'], url=_data['url'], referer=_data['referer'],
            content_type=_data['content_type'], response=_data['response'], response_exists_sensitive=_data['response_exists_sensitive'],
            response_sensitive=_data['response_sensitive'],
            path=_data['path'], path_exist_sensitive=_data['path_exist_sensitive'], path_sensitive=_data['path_sensitive'],
            get_params=_data['get_params'], get_exist_sensitive=_data['get_exist_sensitive'], get_sensitive=_data['get_sensitive'],
            post_params=_data['post_params'], post_exist_sensitive=_data['post_exist_sensitive'], post_sensitive=_data['post_sensitive'],
            timestamp=self.timestamp)
        record_check = self.query_record(where="hash='{hash_val}'".format(hash_val=hash_val), fields='id')
        print("record_check===>", len(record_check))
        if len(record_check) == 0:
            try:
                self.db.add_request_record(values=add_data)
            except Exception as e:
                dir_path = "./mitmproxy/" + _data['host'] + "/error/"
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)
                path = _data['url'].split("/")[-1]
                path = path.split("?")[0]
                path = path.replace(".", "_")
                file_path = dir_path + path + "_second_error.txt"
                w_data = {
                    "exception:": str(e),
                    "url": _data['url'],
                    "data_str": add_data_str,
                    "create_time": self.timestamp
                }
                with open(file_path, mode='a+', encoding="utf-8") as f:
                    f.write(Utility.dict2json(w_data))
