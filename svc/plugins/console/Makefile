# Please tweak it to suit your environment and project.  You
# may want to move it to your project's root directory.
#
# SYNOPSIS:
#
#   make [all]  - makes everything.
#   make TARGET - makes the given target.
#   make clean  - removes all files generated by make.


# Where to find user code.

LIB_DIR = ./../../../../library
USER_DIR = ./../../pub
SO_DIR = ./../../console/plugins

THIRD_PATH = $(LIB_DIR)/mylib/public

CUSTOM_THIRD_PATH = $(LIB_DIR)/mylib/third_party

LINK_PATHS = -L./ -L/usr/local/libmemcached-1.0.7/lib/  -L/usr/lib64/mysql -L$(CUSTOM_THIRD_PATH)/librdkafka

# Flags passed to the preprocessor.
CPPFLAGS += -isystem -shared -fPIC -D_DB_POOL_ -D_DEBUG -DUSR_LOG_MSG\
	-D_DIC_POOL_ -D_REENTRANT -D_GNU_SOURCE -DUSR_LOG_ERROR -DUSR_LOG_MSG\
	-DNET_WORK -DHEAD_SHORT -Wall

# Flags passed to the C++ compiler.
CXXFLAGS += -g  -Wextra -pthread -shared -fPIC

# All tests produced by this Makefile.  Remember to add new tests you
# created to the list.
PLUGIN = $(SO_DIR)/console/console.so
                
INCLUDE_PATHS = -I/usr/local/libmemcached-1.0.7/include \
				-I$(LIB_DIR)/BasicCore \
				-I$(THIRD_PATH)\
				-I/usr/local/include\
				-I/usr/include/mysql\
				-I$(USER_DIR)\
				-I$(CUSTOM_THIRD_PATH)/hiredis\
				-I$(CUSTOM_THIRD_PATH)\
				-I$(LIB_DIR)/mylib/base\
				-I$(CUSTOM_THIRD_PATH)/librdkafka/src\
				-I../\
				


# House-keeping build targets.

ALL_HEADERS = $(USER_HEADERS)
all : $(PLUGIN)

clean :
	rm -f $(PLUGIN)  *.o

# Builds gtest.a and gtest_main.a.

# Usually you shouldn't tweak such internal variables, indicated by a
# trailing _.
#GTEST_SRCS_ = $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)

# For simplicity and to avoid depending on Google Test's
# implementation details, the dependencies specified below are
# conservative and not optimized.  This is fine as Google Test
# compiles fast and for ordinary users its source rarely changes.
#gtest-all.o : $(GTEST_SRCS_)
#	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c \
            $(GTEST_DIR)/src/gtest-all.cc

#gtest_main.o : $(GTEST_SRCS_)
#	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c \
            $(GTEST_DIR)/src/gtest_main.cc

#gtest.a : gtest-all.o
#	$(AR) $(ARFLAGS) $@ $^

#gtest_main.a : gtest-all.o gtest_main.o
#	$(AR) $(ARFLAGS) $@ $^

# Builds a sample test.  A test should link with either gtest.a or
# gtest_main.a, depending on whether it defines its own main()
# function.


console_init.o : ./console_init.cc ./console_init.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./console_init.cc $(INCLUDE_PATHS)

console_logic.o : ./console_logic.cc ./console_logic.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./console_logic.cc $(INCLUDE_PATHS)

console_db.o : ./console_db.cc ./console_db.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./console_db.cc $(INCLUDE_PATHS)
	
console_factory.o : ./console_factory.cc ./console_factory.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./console_factory.cc $(INCLUDE_PATHS)

console_infos.o : ./console_infos.cc ./console_infos.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./console_infos.cc $(INCLUDE_PATHS)

console_stock_manager.o : ./console_stock_manager.cc ./console_stock_manager.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./console_stock_manager.cc $(INCLUDE_PATHS)

console_weibo_manager.o : ./console_weibo_manager.cc ./console_weibo_manager.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./console_weibo_manager.cc $(INCLUDE_PATHS)

console_kafka.o : ./console_kafka.cc ./console_kafka.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./console_kafka.cc $(INCLUDE_PATHS)

hexun_task_manager.o : ./hexun_task_manager.cc ./hexun_task_manager.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./hexun_task_manager.cc $(INCLUDE_PATHS)

xueqiu_task_manager.o : ./xueqiu_task_manager.cc ./xueqiu_task_manager.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./xueqiu_task_manager.cc $(INCLUDE_PATHS)

sina_task_manager.o : ./sina_task_manager.cc ./sina_task_manager.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./sina_task_manager.cc $(INCLUDE_PATHS)
	
console_time_manager.o : ./console_time_manager.cc ./console_time_manager.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c ./console_time_manager.cc $(INCLUDE_PATHS)
		
auto_crawler_infos.o :  $(USER_DIR)/logic/auto_crawler_infos.cc $(USER_DIR)/logic/auto_crawler_infos.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/logic/auto_crawler_infos.cc $(INCLUDE_PATHS)
	
mcontainer.o :  $(USER_DIR)/logic/mcontainer.cc $(USER_DIR)/logic/mcontainer.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/logic/mcontainer.cc $(INCLUDE_PATHS)
	
packet_processing.o :  $(USER_DIR)/net/packet_processing.cc $(USER_DIR)/net/packet_processing.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/net/packet_processing.cc $(INCLUDE_PATHS)
	
logic_unit.o :  $(USER_DIR)/logic/logic_unit.cc $(USER_DIR)/logic/logic_unit.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/logic/logic_unit.cc $(INCLUDE_PATHS)

time.o :  $(USER_DIR)/logic/time.cc $(USER_DIR)/logic/time.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/logic/time.cc $(INCLUDE_PATHS)

data_engine.o :  $(USER_DIR)/storage/data_engine.cc $(USER_DIR)/storage/data_engine.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/storage/data_engine.cc $(INCLUDE_PATHS)

data_mysql_engine.o :  $(USER_DIR)/storage/data_mysql_engine.cc $(USER_DIR)/storage/data_mysql_engine.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/storage/data_mysql_engine.cc $(INCLUDE_PATHS)
	
mysql_pool.o :  $(USER_DIR)/storage/mysql_pool.cc $(USER_DIR)/storage/mysql_pool.h
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c $(USER_DIR)/storage/mysql_pool.cc $(INCLUDE_PATHS)
	

$(PLUGIN) : console_init.o  console_logic.o console_db.o console_kafka.o packet_processing.o logic_unit.o time.o xueqiu_task_manager.o\
	auto_crawler_infos.o console_factory.o console_infos.o console_stock_manager.o console_weibo_manager.o\
	hexun_task_manager.o console_time_manager.o mcontainer.o sina_task_manager.o\
	data_engine.o data_mysql_engine.o mysql_pool.o\
	$(CUSTOM_THIRD_PATH)/dmg_fp/lib/dmg_fp.a $(LIB_DIR)/mylib/base/lib/mybase.a $(LIB_DIR)/mylib/third_party/lib/libhiredis.a $(CUSTOM_THIRD_PATH)/lib/librdkafka.a
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) $(LINK_PATHS) -lpthread -lexpat -lrt -ldl -lmysqlclient \
	$^ -o $@
