from loguru import logger

log_level = 'INFO'
all_path = "../logs/all_{time:YYYY-MM-DD}.log"
error_path = "../logs/error_{time:YYYY-MM-DD}.log"

try:
    from config import console_log
except ImportError:
    console_log = False

if not console_log:
    logger.remove(handler_id=None)

logger.add(all_path, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level=log_level)
logger.add(error_path, format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}", level='ERROR')




