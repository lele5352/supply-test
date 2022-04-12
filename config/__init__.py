from config.api_config import url_prefix

env_configs = {
    # 26环境配置
    'test26': {
        'ims_service_prefix': url_prefix.get('ims_service_26'),
        'app_prefix': url_prefix.get('app_26'),
        'delivery_service_prefix': url_prefix.get('delivery_service_26'),
        'receipt_service_prefix': url_prefix.get('receipt_service_26'),
        'transfer_service_prefix': url_prefix.get('transfer_service_26')
    },
    # 25环境配置
    'test25': {
        'ims_service_prefix': url_prefix.get('ims_service_25'),
        'app_prefix': url_prefix.get('app_25'),
        'delivery_service_prefix': url_prefix.get('delivery_service_25'),
        'receipt_service_prefix': url_prefix.get('receipt_service_25'),
        'transfer_service_prefix': url_prefix.get('transfer_service_25')
    },
    # 160环境配置
    'test160': {
        'ims_service_prefix': url_prefix.get('ims_service_160'),
        'app_prefix': url_prefix.get('app_160'),
        'delivery_service_prefix': url_prefix.get('delivery_service_160'),
        'receipt_service_prefix': url_prefix.get('receipt_service_160'),
        'transfer_service_prefix': url_prefix.get('transfer_service_160')
    }
}

mysql_config = {
    'test163': {
        'user': 'app',
        'passwd': '123456',
        'host': '10.0.0.163',
        'port': 3306
    },
    'test72': {
        'user': 'root',
        'passwd': '123456',
        'host': '10.0.0.72',
        'port': 3306
    },
    'test26': {
        'user': 'app',
        'passwd': '123456',
        'host': '10.0.0.26',
        'port': 3306
    },
    'test160': {
        'user': 'erp',
        'password': 'sd)*(YSHDG;l)D_FKds:D#&y}',
        'host': '10.0.0.127',
        'port': 3306
    },
}
