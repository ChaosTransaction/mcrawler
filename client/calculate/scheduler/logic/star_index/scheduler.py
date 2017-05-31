# -*- coding: utf-8 -*-

"""
Created on 2017年5月23日

@author: kerry
"""
from calculate.scheduler.logic.star_index.storager_manager import Storager
from tools.common.operationcode import storage_opcode
import time

class Scheduler(object):
    def __init__(self,config):
        self._weibo_index = {}  # 微博指数保留最新一小时的热度
        self._volume = {}  # 成交量
        self._buy_linked_price = {}  # 买入挂单价
        self._sell_linked_price = {}  # 卖出挂单价
        self.__last_star_value = {}  # 上一个时间明星的价值分数
        self.__create_selector()

        tconfig = config.get('result')
        if tconfig is not None:
            mconfig = tconfig.get(60009)
            if mconfig is not None:
                self.storager = Storager(mconfig)

    def __set_weibo_index(self, index, data):
        if not data.has_key('hot') or not data.has_key('current'):
            return False
        if self._weibo_index.has_key(index):
            t_data = self._weibo_index[index]
            '''

            if not t_data.has_key('current') or not data.has_key('current'):
                return False
            if t_data['current'] > data['current'] or t_data['current'] == data['current']:
                return False
            '''

        self._weibo_index[index] = data
        return True

    def __set_volume(self, index, volume):
        self._volume[index] = volume

    def __set_buy_linked_price(self, index, buy_linked_price):
        self._buy_linked_price[index] = buy_linked_price

    def __set_sell_linked_price(self, index, sell_linked_price):
        self._sell_linked_price[index] = sell_linked_price

    def __create_selector(self):
        self.logic_function = {1: self.__set_weibo_index,
                               2: self.__set_buy_linked_price,
                               3: self.__set_sell_linked_price,
                               4: self.__set_volume}

    def __recalculate_star_value(self, index):
        weibo_index = self._weibo_index[index].get('hot') if self._weibo_index.has_key(index) else 0
        buy_linked_price = self._buy_linked_price[index] if self._buy_linked_price.has_key(index) else 0
        sell_linked_price = self._sell_linked_price[index] if self._sell_linked_price.has_key(index) else 0
        volume = self._volume[index] if self._volume.has_key(index) else 0
        # 初始化暂无其他值,随意填充
        price = weibo_index * 0.15 + buy_linked_price * 0.2 + sell_linked_price * 0.2 + volume * 0.45
        # price + change
        last_price = self.__last_star_value[index] if self.__last_star_value.has_key(index) else 0
        change = price - last_price
        value = {'symbol': str(index), 'current_price': price, 'change': change, 'current_unix_time': int(time.time())}
        storage_dict = {storage_opcode.kafka_p: value}
        self.storager.star_index(storage_dict)
        self.__last_star_value[index] = last_price

    def process_data(self, data):
        if not data.has_key('index'):
            return None
        else:
            index = data['index']
        if not data.has_key('type'):
            return None
        else:
            type = data['type']

        function = self.logic_function[type]
        if function:
            r = function(index, data)
            if r:
                self.__recalculate_star_value(index)
