from config.mysql_config import mysql_config
from config.api_config import url_prefix

env_configs = {
    # 26环境配置
    'test26': {
        'ims_service_prefix': url_prefix.get('ims_service_26'),
        'app_prefix': url_prefix.get('app_26'),
        'delivery_service_prefix': url_prefix.get('delivery_service_26'),
        'receipt_service_prefix': url_prefix.get('receipt_service_26'),
        'transfer_service_prefix': url_prefix.get('transfer_service_26'),

        'mysql_info_scm': {'mysql_info': mysql_config.get('test_72'), 'db': 'homary_scm'},
        'mysql_info_ims': {'mysql_info': mysql_config.get('test_72'), 'db': 'homary_ims'},
        'mysql_info_oms': {'mysql_info': mysql_config.get('test_72'), 'db': 'ec_oms_26'},
        'mysql_info_wms': {'mysql_info': mysql_config.get('test_163'), 'db': 'supply_wms'},
        'mysql_info_auth': {'mysql_info': mysql_config.get('test_163'), 'db': 'supply_auth'}
    },
    # 160环境配置
    'test160': {
        'ims_service_prefix': url_prefix.get('ims_service_160'),
        'app_prefix': url_prefix.get('app_160'),
        'delivery_service_prefix': url_prefix.get('delivery_service_160'),
        'receipt_service_prefix': url_prefix.get('receipt_service_160'),
        'transfer_service_prefix': url_prefix.get('transfer_service_160'),

        'mysql_info_scm': {'mysql_info': mysql_config.get('test_160'), 'db': 'supply_scm'},
        'mysql_info_ims': {'mysql_info': mysql_config.get('test_160'), 'db': 'supply_ims'},
        'mysql_info_oms': {'mysql_info': mysql_config.get('test_160'), 'db': 'supply_oms'},
        'mysql_info_wms': {'mysql_info': mysql_config.get('test_160'), 'db': 'supply_wms'},
        'mysql_info_auth': {'mysql_info': mysql_config.get('test_160'), 'db': 'supply_auth'}
    }
}
