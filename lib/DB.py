import traceback
import os
import pymysql
from dotenv import find_dotenv, load_dotenv

load_dotenv(find_dotenv('.env'))
env = os.environ


class DB:
    conn = None
    closeFlag = False

    # constructor
    def __init__(self):
        # open db
        try:
            self.conn = self.to_connect()
        except Exception as e:
            print("Exception: Can not connect to MySQL database.")
            exit(0)

    # destructor
    def __del__(self):
        # if self.closeFlag:
        #     self.conn['cursor'].close()
        #     self.conn['db'].close()
        try:
            self.close()
        except Exception as e:
            print(str(e))
            exit(0)

    def to_connect(self):
        db = pymysql.connect(host=env.get("MYSQL_HOST"), user=env.get("MYSQL_USER"), password=env.get("MYSQL_PWD"),
                             database=env.get("MYSQL_DB"), charset='utf8', autocommit=True)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        return {
            'db': db,
            'cursor': cursor
        }

    def close(self):
        # self.closeFlag = True
        if self.conn:
            self.conn['cursor'].close()
            self.conn['db'].close()

    def is_connected(self):
        """Check if the server is alive"""
        try:
            self.conn['db'].ping(reconnect=True)
            # print("db is connecting")
        except:
            traceback.print_exc()
            self.conn = self.to_connect()
            # print("db reconnect")

    def __add(self, table, fields, values):
        self.is_connected()
        # print(values)
        sql = "insert into " + table + "(" + fields + ") values(" + values + ")"
        # print("add sql===>>>", sql)
        self.conn['cursor'].execute(sql)

    def add_scanner(self, table='scanner', fields='url,json,create_time', values=''):
        self.__add(table, fields, values)

    def add_request_record(self, table='request_record',
                           fields='flow_id,host,port,hash,'
                                  'method,url,referer,content_type,response,response_exists_sensitive,response_sensitive,'
                                  'path,path_exist_sensitive,path_sensitive,'
                                  'get_params,get_exist_sensitive,get_sensitive,'
                                  'post_params,post_exist_sensitive,post_sensitive,'
                                  'create_time',
                           values=''):
        self.__add(table, fields, values)

    def add_request_record_second(self, table='request_record_second',
                                  fields='host,hash,method,content_type,referer,'
                                         'origin_url,url,response,response_exists_sensitive,response_sensitive,'
                                         'response_hash,gen_params,create_time',
                                  values=''):
        self.__add(table, fields, values)

    # print(values)

    def query(self, sql):
        self.is_connected()
        self.conn['cursor'].execute(sql)
        return self.conn['cursor'].fetchall()
        # data = pd.DataFrame(list(ds), columns=cols)
        # print(data)

    def query_data(self, table, where, fields='*'):
        sql = "select " + fields + " from " + table + " where " + where
        # print("query sql===>>>", sql)
        return self.query(sql)

    def query_request_record(self, where='1=1', fields='*'):
        return self.query_data(table='request_record', where=where, fields=fields)

    def query_request_record_second(self, where='1=1', fields='*'):
        return self.query_data(table='request_record_second', where=where, fields=fields)
