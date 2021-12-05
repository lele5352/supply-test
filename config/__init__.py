from config.mysql_config import mysql_config
from config.api_config import url_prefix

user = {
    'username': 'xuhongwei@popicorns.com',
    'password': '123456'
}

mysql_info = mysql_config.get('test_160')

ims_service_prefix = url_prefix.get('ims_service_160')

app_prefix = url_prefix.get('app_160')

delivery_service_prefix = url_prefix.get('delivery_service_160')

receipt_service_prefix = url_prefix.get('receipt_service_160')

# mysql_info = mysql_config.get('test_160')
#
# mysql_info_72 = mysql_config.get('test_160')
#
# ims_service_prefix = url_prefix.get('ims_service_26')
#
# app_prefix = url_prefix.get('app_26')
#
# delivery_service_prefix = url_prefix.get('delivery_service_26')
#
# receipt_service_prefix = url_prefix.get('receipt_service_26')
