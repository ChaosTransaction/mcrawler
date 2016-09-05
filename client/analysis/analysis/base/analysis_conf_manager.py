# -.- coding:utf-8 -.-
"""
Created on 2015年10月9日

@author: chenyitao
"""

import ConfigParser
import os


class AnalysisConfManager(object):
    """
    class docs
    """

    __conf_path = os.path.dirname(os.path.dirname(__file__)) + '/../analysis.conf'

    def __init__(self):
        """
        Constructor
        """
        self.hbase_info = {}
        self.redis_info = {}
        self.ftp_info = {}
        self.kafka_info = {}
        self.mysql_info = {}
        self.conf_file = ConfigParser.ConfigParser()
        self.conf_file.read(self.__conf_path)
        self.__read_hbase_info()
        self.__read_redis_info()
        self.__read_ftp_info()
        self.__read_kafka_info()
        self.__read_mysql_info()

    def __read_hbase_info(self):
        """
        read hbase info
        """
        host = self.conf_file.get('hbase_info', 'host')
        self.hbase_info['host'] = host
        port = self.conf_file.get('hbase_info', 'port')
        self.hbase_info['port'] = int(port)

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
        
    def __read_kafka_info(self):
        host = self.conf_file.get('kafka_info', 'host')
        self.kafka_info['host'] = host
        name = self.conf_file.get('kafka_info', 'name')
        self.kafka_info['name'] = name

    def __read_mysql_info(self):
        host = self.conf_file.get('mysql_info', 'host')
        self.mysql_info['host'] = host
        username = self.conf_file.get('mysql_info', 'username')
        self.mysql_info['username'] = username
        password = self.conf_file.get('mysql_info', 'password')
        self.mysql_info['password'] = password

analysis_conf = AnalysisConfManager()
