from loguru._logger import Core, Logger
import sys as _sys

log_level = 'INFO'
log_format = "{time:YYYY-MM-DD HH:mm:ss.SSS}|{level}|{message}"
all_path = "../logs/all_{time:YYYY-MM-DD}.log"
error_path = "../logs/error_{time:YYYY-MM-DD}.log"

try:
    from config import console_log
except ImportError:
    console_log = False


NoConsoleLog = Logger(Core(), None, 0, False, False, False, False, True, [], {})
ConsoleLog = Logger(Core(), None, 0, False, False, False, False, True, [], {})

NoConsoleLog.add(all_path, format=log_format,
                 level=log_level)
NoConsoleLog.add(error_path, format=log_format,
                 level='ERROR')

ConsoleLog.add(_sys.stderr)
ConsoleLog.add(all_path, format=log_format,
               level=log_level)
ConsoleLog.add(error_path, format=log_format,
               level='ERROR')


class OutputLog:
    """
    执行日志输出类，根据参数执行是否将日志输出到控制台
    当前只定义最常用的四种级别日志输出：info, error, debug, warning
    """

    @staticmethod
    def info(message, sys_out=console_log, **kwargs):
        """打印 info 级别日志
        :param message: 日志信息
        :param sys_out: bool类型，默认从config取值；
                        True 日志同时输出到文件和控制台，False 只输出到文件
        """
        if sys_out:
            ConsoleLog.info(message, **kwargs)
        else:
            NoConsoleLog.info(message, **kwargs)

    @staticmethod
    def error(message, sys_out=console_log, **kwargs):
        """打印 error 级别日志
        :param message: 日志信息
        :param sys_out: bool类型，默认从config取值；
                        True 日志同时输出到文件和控制台，False 只输出到文件
        """
        if sys_out:
            ConsoleLog.error(message, **kwargs)
        else:
            NoConsoleLog.error(message, **kwargs)

    @staticmethod
    def debug(message, sys_out=console_log, **kwargs):
        """打印 debug 级别日志
        :param message: 日志信息
        :param sys_out: bool类型，默认从config取值；
                        True 日志同时输出到文件和控制台，False 只输出到文件
        """
        if sys_out:
            ConsoleLog.debug(message, **kwargs)
        else:
            NoConsoleLog.debug(message, **kwargs)

    @staticmethod
    def warning(message, sys_out=console_log, **kwargs):
        """打印 warning 级别日志
        :param message: 日志信息
        :param sys_out: bool类型，默认从config取值；
                        True 日志同时输出到文件和控制台，False 只输出到文件
        """
        if sys_out:
            ConsoleLog.warning(message, **kwargs)
        else:
            NoConsoleLog.warning(message, **kwargs)


logger = OutputLog




