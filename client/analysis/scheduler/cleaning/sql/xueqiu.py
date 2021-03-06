# -.- coding:utf-8 -.-
"""
Created on 2016年11月26日

@author: kerry
"""

from analysis.scheduler.fetch.enclosure.sqlite_manage_model import SQLiteStorage
from analysis.db.xueqiu import XueQiu as xqdb
from analysis.base.mlog import mlog
from analysis.comm_opercode import local_task_opercode


class Xueqiu():

    def __init__(self,basic_path):
        self.sql_mgr = None

    def connect(self,file_path):
        self.sql_mgr = SQLiteStorage(file_path, 1)


    def fetchall_data(self, pid):
        dict = {}
        result = self.sql_mgr.get_table()
        for t in result:
            s_t = "".join(t)
            mlog.log().info("tablename %s ", s_t)
            if pid == local_task_opercode.XUEQIU_GET_MEMBER_MAX:
                sql = xqdb.get_member_max(s_t)
            elif pid ==  pid == local_task_opercode.XUEQIU_GET_DISCUSSION_UID:
                sql = xqdb.get_user_discuss_max(s_t)
            else:
                sql = xqdb.get_id(s_t)
            dict[s_t] = self.sql_mgr.get_data(sql)
        return dict


