import logging
import logging.handlers
import time
import os


class LoggerHandler:
    def __init__(self, filename):
        # 定义对应的程序模块名name，默认为root
        self.logger = logging.getLogger()
        self.logger.handlers.clear()
        # log_path是存放日志的路径
        time_str = time.strftime('%Y_%m_%d', time.localtime(time.time()))
        lib_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../logs'))
        # 如果不存在这个logs文件夹，就自动创建一个
        if not os.path.exists(lib_path):
            os.mkdir(lib_path)
        # 日志文件的地址
        log_name = lib_path + '/' + filename + '_' + time_str + '.log'

        # 必须设置，这里如果不显示设置，默认过滤掉warning之前的所有级别的信息
        self.logger.setLevel(logging.INFO)

        # 日志输出格式
        formatter = logging.Formatter('[%(asctime)s | %(levelname)s | %(message)s')

        # 创建一个FileHandler， 向文件logname输出日志信息
        fh = logging.FileHandler(log_name, 'a', encoding='utf-8')

        # 设置日志等级
        fh.setLevel(logging.INFO)
        # 设置handler的格式对象
        fh.setFormatter(formatter)
        # 将handler增加到logger中
        self.logger.addHandler(fh)

        # 创建一个StreamHandler,用于输出到控制台
        # ch = logging.StreamHandler()
        # ch.setLevel(logging.INFO)
        # ch.setFormatter(formatter)
        # self.logger.addHandler(ch)

        # 关闭打开的文件
        fh.close()

    def log(self, message, level=''):
        if level == 'WARNING':
            self.logger.warning(message)
        elif level == 'ERROR':
            self.logger.error(message)
        elif level == 'DEBUG':
            self.logger.debug(message)
        elif level == 'CRITICAL':
            self.logger.critical(message)
        else:
            self.logger.info(message)


if __name__ == "__main__":
    log_handler = LoggerHandler('test')
    log_handler.log('test1')
    log_handler.log('test2', 'WARNING')
    log_handler.log('test3', 'ERROR')
    log_handler.log('test4', 'CRITICAL')
