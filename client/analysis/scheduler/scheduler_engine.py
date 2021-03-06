# -*- coding: utf-8 -*-

'''
Created on 2017-05-23
@author kerry
'''
from analysis.parser.parser import Parser as MParser
from analysis.scheduler.fetch.fetch_manage import FetchFileManager
from analysis.scheduler.input.input_manage import InputManager
from analysis.scheduler.logic.schedule_engine import ScheduleEngine as LGSchedulerEngine


class ScheduleEngine:
    def __init__(self, config):
        self.parser = MParser()
        self.task_queue = []
        self.recovery_file = {}
        self.fetch_mgr = FetchFileManager()
        self.scheduler = LGSchedulerEngine(config)
        self.config = config
        self.input_mgr = InputManager(config)

    def __del__(self):
        pass

    def start(self, func_callback=None):
        if func_callback is not None:
            self.input_mgr.start(func_callback)
        else:
            self.input_mgr.start()

    def input_data(self, path, filename=None):
        if filename is None:
            return self.input_mgr.get_alldata(path)
        else:
            return self.input_mgr.get_data(path, filename)

    """
    解析数据
    """

    def __data_parser(self, content, pltid):
        # data = CleaningCrawler.clean_data(content)
        if content is not None:
            return self.parser.parse(pltid, content)
        else:
            return {'status': -1}

    """
    拉取文件转化为数据
    """

    def __process_fetch_file(self, pid, ftype, basic_path, file_name, fid):
        return self.fetch_mgr.process_data(ftype, basic_path, file_name, fid)

    def __process_file(self, pid, ftype, basic_path, file_name, fid):
        data = self.__process_fetch_file(pid, ftype, basic_path, file_name, fid)
        parser_dict = self.__data_parser(data, pid)

        """
        根据平台id,传递给管理类
        """
        if parser_dict['status'] == 1:
            self.scheduler.process_data(pid, parser_dict)

    """
    单进程处理文件
    """

    def process_file_data(self, pid, basic_path, file_name, ftype, fid=0):
        self.__process_file(pid, ftype, basic_path, file_name, fid)

    """
    多线程处理文件
    """