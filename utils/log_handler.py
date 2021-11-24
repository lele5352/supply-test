import logging.handlers
import datetime
import time
import os
logger = logging.getLogger('supply_log')
logger.setLevel(logging.INFO)

# log_path是存放日志的路径
time_str = time.strftime('%Y%m%d', time.localtime(time.time()))
lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
# 如果不存在这个logs文件夹，就自动创建一个
if not os.path.exists(lib_path):
    os.mkdir(lib_path)
# 日志文件的地址
all_log_name = lib_path + '/' + 'all' + '_' + time_str + '.log'
error_log_name = lib_path + '/' + 'error' + '_' + time_str + '.log'
# 全部log
rf_handler = logging.FileHandler(all_log_name)
rf_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))

# 错误log
f_handler = logging.FileHandler(error_log_name)
f_handler.setLevel(logging.ERROR)
f_handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(filename)s[:%(lineno)d] - %(message)s"))

logger.addHandler(rf_handler)
logger.addHandler(f_handler)

if __name__ == "__main__":
    logger.debug('test1')
    logger.warning('test2')
    logger.error('test3')
    logger.critical('test4')