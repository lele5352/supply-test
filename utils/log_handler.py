from loguru import logger

log_level = 'INFO'

logger.add("../logs/all_{time:YYYY-MM-DD}.log",
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
           level=log_level)

logger.add("../logs/error_{time:YYYY-MM-DD}.log",
           format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
           level='ERROR')

