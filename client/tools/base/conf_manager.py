# -.- coding:utf-8 -.-
"""
Created on 2017年5月25日

@author: kerry
"""

import ConfigParser
import os

class ConfManager(object):
    """
    class docs
    """
    # 定义静态变量实例
    __singleton = None
    @staticmethod
    def get_instance():
        if ConfManager.__singleton is None:
            ConfManager.__singleton = ConfManager()
        return ConfManager.__singleton

    def __init__(self):
        pass

    def init(self,file,filer_code):
        #self.__conf_path = os.path.dirname(os.path.dirname(__file__)) + file
        self.__conf_path = file
        self.__filer_code = filer_code
        self.hbase_info = {}
        self.redis_info = {}
        self.ftp_info = {}
        self.kafka_info = {}
        self.local_info = {}
        self.conf_file = ConfigParser.ConfigParser()
        self.conf_file.read(self.__conf_path)
        self.__read_hbase_info()
        self.__read_redis_info()
        self.__read_ftp_info()
        self.__read_kafka_info()
        self.__read_local_info()


    def __read_hbase_info(self):
        """
        read hbase info
        """
        host = self.conf_file.get('hbase_info', 'host')
        self.hbase_info['host'] = host
        port = self.conf_file.get('hbase_info', 'port')
        self.hbase_info['port'] = int(port)
        self.hbase_info['type'] = int(self.__filer_code.hbase)

    def __read_redis_info(self):
        """
        read redis info
        """
        host = self.conf_file.get('redis_info', 'host')
        self.redis_info['host'] = host
        port = self.conf_file.get('redis_info', 'port')
        self.redis_info['port'] = int(port)
        db = self.conf_file.get('redis_info', 'db')
        self.redis_info['db'] = int(db)
        password = self.conf_file.get('redis_info', 'password')
        self.redis_info['password'] = password
        self.redis_info['type'] = int(self.__filer_code.redis)

    def __read_ftp_info(self):
        """
        read ftp info
        """
        host = self.conf_file.get('ftp_info', 'host')
        self.ftp_info['host'] = host
        port = self.conf_file.get('ftp_info', 'port')
        self.ftp_info['port'] = int(port)
        user = self.conf_file.get('ftp_info', 'user')
        self.ftp_info['user'] = user
        passwd = self.conf_file.get('ftp_info', 'passwd')
        self.ftp_info['passwd'] = passwd
        timeout = self.conf_file.get('ftp_info', 'timeout')
        self.ftp_info['timeout'] = int(timeout)
        local = self.conf_file.get('ftp_info', 'local')
        self.ftp_info['local'] = local
        self.ftp_info['type'] = int(self.__filer_code.ftp)
        
    def __read_kafka_info(self):
        host = self.conf_file.get('kafka_info', 'host')
        self.kafka_info['host'] = host
        name = self.conf_file.get('kafka_info', 'name')
        self.kafka_info['name'] = name
        self.kafka_info['type'] = int(self.__filer_code.kafka)

    def __read_local_info(self):
        path = self.conf_file.get('local_info', 'path')
        self.local_info['path'] = path
        self.local_info['type'] = int(self.__filer_code.local)

#conf = ConfManager()
