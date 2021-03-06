# -.- coding:utf-8 -.-
"""
Created on 2016年11月18日

@author: kerry
"""


from analysis.common.ftp_manager import FTPManager
from analysis.base.analysis_conf_manager import analysis_conf
from analysis.common.mstring import MString
from analysis.scheduler.cleaning.cralwer.cleaning import CleaningCrawler


"""
ftp:
file: ftp路径
pltid: 平台id
"""

class FtpEngine:

    def __init__(self, num = 4):

        self.ftp_mgr = FTPManager(analysis_conf.ftp_info['host'],
                                  analysis_conf.ftp_info['port'],
                                  analysis_conf.ftp_info['user'],
                                  analysis_conf.ftp_info['passwd'],
                                  analysis_conf.ftp_info['local'])

        self.ftp_mgr.connect()
        #self.ftp_pool = FtpPoolManager(num * 4)


    def __del__(self):
        self.ftp_mgr.close()


    def __clean_data(self,content):
        return CleaningCrawler.clean_data(content)



    def fetch_data(self, basic_path, file_name):
        ftp_url = basic_path + "/" + file_name
        ftp_objstring = MString(file_name) #ftp文本文件处理
        #if self.ftp_mgr.get(ftp_url, ftp_objstring.write):
        if self.ftp_mgr.get(basic_path, file_name, ftp_objstring.write):
            # 数据清洗
            return self.__clean_data(ftp_objstring.string)
        else:
            return None

    def process(self, basic_path, pid, file_name): #用于单线程获取数据
        return self.fetch_data(basic_path, file_name)




