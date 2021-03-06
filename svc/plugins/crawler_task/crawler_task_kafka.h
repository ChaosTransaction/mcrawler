//  Copyright (c) 2015-2018 The KID Authors. All rights reserved.
//  Created on: 2016.2.18 Author: yangge

#ifndef KID_CRAWLER_TASK_KAFKA_H_
#define KID_CRAWLER_TASK_KAFKA_H_

#include "basic/basictypes.h"
#include "basic/scoped_ptr.h"
#include "logic/auto_crawler_infos.h"
#include "logic/base_values.h"
#include "queue/kafka_consumer.h"
#include <list>
#include <map>
#include <string>

namespace crawler_task_logic {

class CrawlerTaskKafka {
 public:
  CrawlerTaskKafka(config::FileConfig *config);
  CrawlerTaskKafka(const int32 svc_id, base::ConnAddr& addr);
  virtual ~CrawlerTaskKafka();

 public:
  bool FectchBatchTempTask(std::list<base_logic::TaskInfo> *list);

  void SetTaskInfo(base_logic::TaskInfo &task_info,
                   base_logic::DictionaryValue *task_info_dic);

 private:
  kafka_consumer kafka_consumer_;
};
}  // namespace crawler_task_logic

#endif /* TASK_DB_H_ */
