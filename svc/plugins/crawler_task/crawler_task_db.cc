//  Copyright (c) 2015-2015 The KID Authors. All rights reserved.
//  Created on: 2015.9.22 Author: kerry

#include "crawler_task/crawler_task_db.h"
#include "basic/basic_util.h"
#include "basic/radom_in.h"
#include "basic/template.h"
#include "logic/logic_comm.h"
#include "logic/logic_unit.h"
#include <mysql.h>
#include <set>
#include <sstream>

namespace crawler_task_logic {

CrawlerTaskDB::CrawlerTaskDB(config::FileConfig *config) {
  // mysql_engine_.reset(base_logic::DataControllerEngine::Create(MYSQL_TYPE));
  mysql_engine_ = base_logic::DataEngine::Create(MYSQL_TYPE);
  mysql_engine_->InitParam(config->mysql_db_list_);
  task_platform_inited_ = false;
}

CrawlerTaskDB::~CrawlerTaskDB() {
  if (mysql_engine_) {
    delete mysql_engine_;
    mysql_engine_ = NULL;
  }
  LOG_MSG("~CrawlerTaskDB()");
}

bool CrawlerTaskDB::FetchBatchTask(std::list<base_logic::TaskInfo> *list,
                                   const bool is_new) {
  bool r = false;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());

  std::string sql;
  if (is_new)
    sql = "call proc_FetchNewTask()";
  else
    sql = "call proc_FetchBatchTask()";
  base_logic::ListValue *listvalue;
  dict->SetString(L"sql", sql);
  r = mysql_engine_->ReadData(0, (base_logic::Value *)(dict.get()),
                              CallBackFectchBatchTask);
  if (!r)
    return false;
  dict->GetList(L"resultvalue", &listvalue);
  while (listvalue->GetSize()) {
    base_logic::TaskInfo task;
    base_logic::Value *result_value;
    listvalue->Remove(0, &result_value);
    base_logic::DictionaryValue *dict_result_value =
        (base_logic::DictionaryValue *)(result_value);
    task.ValueSerialization(dict_result_value);
    task.set_type(MAIN_LASTING_TASK);
    list->push_back(task);
    delete dict_result_value;
    dict_result_value = NULL;
  }

  return true;
}

bool CrawlerTaskDB::RecordTaskState(base_logic::TaskInfo &task,
                                    const int32 type) {
  bool r = false;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());
  std::string sql;
  sql =
      "call proc_RecordTaskState(" +
      base::BasicUtil::StringUtil::Int64ToString(task.id()) + "," +
      base::BasicUtil::StringUtil::Int64ToString(
          static_cast<int64>(task.state())) +
      "," + base::BasicUtil::StringUtil::Int64ToString(task.last_task_time()) +
      "," + base::BasicUtil::StringUtil::Int64ToString((task.polling_time())) +
      "," + base::BasicUtil::StringUtil::Int64ToString(time(NULL)) + "," +
      base::BasicUtil::StringUtil::Int64ToString(type) + ")";
  base_logic::ListValue *listvalue;
  dict->SetString(L"sql", sql);
  r = mysql_engine_->WriteData(0, (base_logic::Value *)(dict.get()));
  if (!r)
    return false;

  return true;
}

void CrawlerTaskDB::CreateTaskLog(const int32 id,
                                  std::list<base_logic::TaskInfo> *list) {
  bool r = false;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());

  while (list->size()) {
    std::string sql;
    base_logic::TaskInfo task = list->front();
    list->pop_front();
    sql = "call proc_CreateTaskLog(" +
          base::BasicUtil::StringUtil::Int64ToString(id) + "," +
          base::BasicUtil::StringUtil::Int64ToString(task.id()) + "," +
          base::BasicUtil::StringUtil::Int64ToString(task.attrid()) + "," +
          base::BasicUtil::StringUtil::Int64ToString(task.last_task_time()) +
          "," + base::BasicUtil::StringUtil::Int64ToString(task.machine()) +
          "," + base::BasicUtil::StringUtil::Int64ToString(task.method()) +
          ",'" + task.url().c_str() + "');";
    base_logic::ListValue *listvalue;
    dict->SetString(L"sql", sql);
    r = mysql_engine_->WriteData(0, (base_logic::Value *)(dict.get()));
  }
  return;
}

void CrawlerTaskDB::CreateTaskLog(const int32 id, base_logic::TaskInfo &task) {
  bool r = false;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());
  std::string sql;

  // call
  // crawler.proc_CreateTaskLog(111111,3,1472350855,1,1,'http://www.baidu.com')
  sql = "call proc_CreateTaskLog(" +
        base::BasicUtil::StringUtil::Int64ToString(id) + "," +
        base::BasicUtil::StringUtil::Int64ToString(task.id()) + "," +
        base::BasicUtil::StringUtil::Int64ToString(task.attrid()) + "," +
        base::BasicUtil::StringUtil::Int64ToString(task.last_task_time()) +
        "," + base::BasicUtil::StringUtil::Int64ToString(task.machine()) + "," +
        base::BasicUtil::StringUtil::Int64ToString(task.method()) + ",'" +
        task.url().c_str() + "')";
  base_logic::ListValue *listvalue;
  dict->SetString(L"sql", sql);
  r = mysql_engine_->WriteData(0, (base_logic::Value *)(dict.get()));

  return;
}

void CrawlerTaskDB::UpdateTaskLog(const int64 task_id, const int8 state) {
  bool r = false;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());
  std::string sql;

  // call crawler.proc_UpdateTaskType(111111,2)
  sql = "call proc_UpdateTaskType(" +
        base::BasicUtil::StringUtil::Int64ToString(task_id) + "," +
        base::BasicUtil::StringUtil::Int64ToString(state) + ")";
  base_logic::ListValue *listvalue;
  dict->SetString(L"sql", sql);
  r = mysql_engine_->WriteData(0, (base_logic::Value *)(dict.get()));
  return;
}

void CrawlerTaskDB::CallBackFectchBatchTask(void *param,
                                            base_logic::Value *value) {
  base_logic::DictionaryValue *dict = (base_logic::DictionaryValue *)(value);
  base_logic::ListValue *list = new base_logic::ListValue();
  base_storage::DBStorageEngine *engine =
      (base_storage::DBStorageEngine *)(param);
  MYSQL_ROW rows;
  int32 num = engine->RecordCount();
  if (num > 0) {
    while (rows = (*(MYSQL_ROW *)(engine->FetchRows())->proc)) {
      base_logic::DictionaryValue *info_value =
          new base_logic::DictionaryValue();
      if (rows[0] != NULL)
        info_value->SetBigInteger(L"id", atoll(rows[0]));
      if (rows[1] != NULL)
        info_value->SetBigInteger(L"attrid", atoll(rows[1]));
      if (rows[2] != NULL)
        info_value->SetCharInteger(L"depth",
                                   logic::SomeUtils::StringToIntChar(rows[2]));
      if (rows[3] != NULL)
        info_value->SetCharInteger(L"machine",
                                   logic::SomeUtils::StringToIntChar(rows[3]));
      if (rows[4] != NULL)
        info_value->SetCharInteger(L"storage",
                                   logic::SomeUtils::StringToIntChar(rows[4]));
      if (rows[5] != NULL)
        info_value->SetCharInteger(L"islogin",
                                   logic::SomeUtils::StringToIntChar(rows[5]));
      if (rows[6] != NULL)
        info_value->SetCharInteger(L"isforge",
                                   logic::SomeUtils::StringToIntChar(rows[6]));
      if (rows[7] != NULL)
        info_value->SetCharInteger(L"isover",
                                   logic::SomeUtils::StringToIntChar(rows[7]));
      if (rows[8] != NULL)
        info_value->SetCharInteger(L"method",
                                   logic::SomeUtils::StringToIntChar(rows[8]));
      if (rows[9] != NULL)
        info_value->SetBigInteger(L"polling_time", atoll(rows[9]) / 2);
      if (rows[10] != NULL)
        info_value->SetString(L"url", rows[10]);
      list->Append((base_logic::Value *)(info_value));
    }
  }
  dict->Set(L"resultvalue", (base_logic::Value *)(list));
}

bool CrawlerTaskDB::GetTaskPlatTaskDescription(
    std::list<base_logic::TaskPlatDescription> *list) {
  //  call crawler.proc_GetTaskPlatInfo()
  bool r = false;
  scoped_ptr<base_logic::DictionaryValue> dict(
      new base_logic::DictionaryValue());
  std::string sql = "call proc_GetTaskPlatInfo()";
  base_logic::ListValue *listvalue;
  dict->SetString(L"sql", sql);
  r = mysql_engine_->ReadData(0, (base_logic::Value *)(dict.get()),
                              CallBackGetTaskPlatDescription);
  if (!r)
    return false;

  dict->GetList(L"resultvalue", &listvalue);
  while (listvalue->GetSize()) {
    base_logic::TaskPlatDescription description;
    base_logic::Value *result_value;
    listvalue->Remove(0, &result_value);
    description.ValueSerialization(
        (base_logic::DictionaryValue *)(result_value));
    list->push_back(description);
  }
  return true;
}

void CrawlerTaskDB::CallBackGetTaskPlatDescription(void *param,
                                                   base_logic::Value *value) {
  base_logic::DictionaryValue *dict = (base_logic::DictionaryValue *)(value);
  base_logic::ListValue *list = new base_logic::ListValue();
  base_storage::DBStorageEngine *engine =
      (base_storage::DBStorageEngine *)(param);
  MYSQL_ROW rows;
  int32 num = engine->RecordCount();
  if (num > 0) {
    while (rows = (*(MYSQL_ROW *)(engine->FetchRows())->proc)) {
      base_logic::DictionaryValue *info_value =
          new base_logic::DictionaryValue();
      if (rows[0] != NULL)
        info_value->SetBigInteger(L"id", atoll(rows[0]));
      if (rows[1] != NULL)
        info_value->SetCharInteger(L"depth",
                                   logic::SomeUtils::StringToIntChar(rows[1]));
      if (rows[2] != NULL)
        info_value->SetCharInteger(L"machine",
                                   logic::SomeUtils::StringToIntChar(rows[2]));
      if (rows[3] != NULL)
        info_value->SetCharInteger(L"storage",
                                   logic::SomeUtils::StringToIntChar(rows[3]));
      if (rows[4] != NULL)
        info_value->SetCharInteger(L"isforge",
                                   logic::SomeUtils::StringToIntChar(rows[4]));
      if (rows[5] != NULL)
        info_value->SetCharInteger(L"isover",
                                   logic::SomeUtils::StringToIntChar(rows[5]));
      if (rows[6] != NULL)
        info_value->SetString(L"description", rows[6]);
      list->Append((base_logic::Value *)(info_value));
    }
  }
  dict->Set(L"resultvalue", (base_logic::Value *)(list));
}

void CrawlerTaskDB::BatchFectchTaskPlatInfo(
    std::list<base_logic::TaskPlatDescription> *list) {
  while ((*list).size() > 0) {
    base_logic::TaskPlatDescription info = (*list).front();
    (*list).pop_front();
    task_platform_[info.id()] = info;
  }
}

void CrawlerTaskDB::BatchUpdateTaskInfo(std::list<base_logic::TaskInfo> *list) {
  if (!task_platform_inited_) {
    std::list<base_logic::TaskPlatDescription> list;
    GetTaskPlatTaskDescription(&list);
    BatchFectchTaskPlatInfo(&list);
    task_platform_inited_ = true;
  }
  std::list<base_logic::TaskInfo>::iterator it = (*list).begin();
  for (; it != (*list).end(); it++) {
    bool r = false;
    base_logic::TaskInfo info = (*it);
    base_logic::TaskPlatDescription descripition;
    r = base::MapGet<TASKPLAT_MAP, TASKPLAT_MAP::iterator, int64,
                     base_logic::TaskPlatDescription>(
        task_platform_, info.attrid(), descripition);
    if (r) {
      info.set_is_forge(descripition.forge());
      info.set_machine(descripition.machine());
      info.set_storage(descripition.storage());
      info.set_is_over(descripition.over());
    } else {
      //  若id不存在，则需到数据库获取 是否有新的
      continue;
    }
  }
}

} // namespace crawler_task_logic
