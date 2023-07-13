prefix_config = {
    # 26环境配置
    'test26': {
        'ims': 'http://10.0.0.26:28801',
        'app': 'https://test-26.popicorns.com',
        'delivery': 'http://10.0.0.26:8330',
        'receipt': 'http://10.0.0.26:8323',
        'transfer': 'http://10.0.0.26:8334'
    },
    # 25环境配置
    'test25': {
        'ims_service_prefix': 'http://10.0.0.25:28801',
        'app': 'https://test-25.popicorns.com',
        'delivery_service_prefix': 'http://10.0.0.25:8330',
        'receipt_service_prefix': 'http://10.0.0.25:8323',
        'transfer_service_prefix': 'http://10.0.0.25:8334'
    },
    # 160环境配置
    'test160': {
        'ims': 'http://10.0.0.159:28801',
        'app': 'https://test-scms.popicorns.com',
        'wms_base': 'http://10.0.0.160:8321',
        'delivery': 'http://10.0.0.160:8330',
        'receipt': 'http://10.0.0.160:8323',
        'transfer': 'http://10.0.0.160:8334',
        'oms_app': 'http://10.0.0.160:8826',
        'eta': 'http://10.0.0.159:8701',
    },
    'test189': {
        'ims': 'http://10.0.0.189:28801',
        'app': 'https://test189.popicorns.com',
        'wms_base': 'http://10.0.0.189:8321',
        'delivery': 'http://10.0.0.189:8330',
        'receipt': 'http://10.0.0.189:8323',
        'transfer': 'http://10.0.0.189:8334',
        'oms_app': 'http://10.0.0.189:8826',
        'eta': 'http://10.0.0.189:8701',
    },
    # uat环境配置
    'uat': {
        'ims': 'http://10.0.15.21:28801',
        'app': 'https://uat-scms.popicorns.com',
        'delivery': 'http://10.0.15.21:8330',
        'receipt': 'http://10.0.15.21:8323',
        'transfer': 'http://10.0.15.21:8334',
        'eta': 'http://10.0.0.159:8701',
    },
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
        'host': '10.0.0.163',
        'port': 3306
    },
    'test160': {
        "scms":
            {
                'user': 'erp',
                'password': 'sd)*(YSHDG;l)D_FKds:D#&y}',
                'host': '10.0.0.127',
                'port': 3306
            },
        "tms":
            {
                'user': 'erp',
                'password': 'sd)*(YSHDG;l)D_FKds:D#&y}',
                'host': '10.0.0.156',
                'port': 3306
            }
    },
    'test189': {
        "scms":
            {
                'user': 'erp',
                'password': 'sd)*(YSHDG;l)D_FKds:D#&y}',
                'host': '10.0.0.190',
                'port': 3306
            },
        "tms":
            {
                'user': 'erp',
                'password': 'sd)*(YSHDG;l)D_FKds:D#&y}',
                'host': '10.0.0.190',
                'port': 3306
            }
    },
    'uat': {
        'user': 'erp',
        'password': 'sd)*(YSHDG;l)D_FKds:D#&y}',
        'host': '10.0.15.21',
        'port': 3301
    },
}
