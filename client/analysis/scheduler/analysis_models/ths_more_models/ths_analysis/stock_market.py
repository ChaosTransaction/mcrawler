# -.- coding:utf-8 -.-
"""
Created on 2015年12月28日

@author: slm
"""
import urllib2
import os
import traceback
from lxml import html
from scheduler.analysis_models.ths_more_models.ths_analysis.more_news_base import MoreNewsBase


class THSStockMarket(MoreNewsBase):
    """
    股票-市场（8.市场频道）(利用源代码解析)
    """
    tag = {'rule': '/html/head/title',
           'tag': '市场频道-股市,股票市场,今日股市行情,股市行情大盘,今日股市最新消息_同花顺财经'}

    def __init__(self, callback=None, **kwargs):
        """
        Constructor
        """
        super(self.__class__, self).__init__(callback, **kwargs)
        self.storage_type = 1
        self._type = '股票市场'
        self.analyzed_info_list = []
        self.__analysis()
        self.analyzed()

    def __analysis(self):
        """
        解析
        """
#         with open('./ths_market.html', 'r') as f:
#             self.html_data = f.read()
        try:
            self.html_data = self.gz_decode(self.html_data)
        except:
            traceback.print_exc()
        doc = html.fromstring(self.html_data)
        self.__live_stock(doc)
        self.__section_focus(doc)

    def __live_stock(self, doc):
        """
        股市直播
        """
        model = '股市直播'
        more_news = doc.xpath(r'//div[@id="dpfx_div"]//li[@class="new_tylt"]//a')
        for new in more_news:
            title = new.xpath(r'@title')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)

    def __section_focus(self, doc):
        """
        版块聚焦
        """
        model = '版块聚焦'
        more_news = doc.xpath(r'//div[@id="bkfocus_div"]//li[@class="new_tylt"]//a')
        for new in more_news:
            title = new.xpath(r'@title')[0]
            url = new.xpath(r'@href')[0]
            self.set_analyzed_info(title, self._type, model, None, url)


def load_data():
    """
    加载网页html
    """
    if not os.path.exists('./ths_market.html'):
        response = urllib2.urlopen('http://stock.10jqka.com.cn/market.shtml')
        with open('./ths_market.html', 'w') as f:
            f.write(response.read())


def main():
    """
    执行
    """
    analysis = THSStockMarket()
    for info in analysis.analyzed_info_list:
        print info.title
        print info.url
        print info.model
        print info.type
        print '============'
    print analysis

if __name__ == '__main__':
    load_data()
    main()