class ServerInfoConfig:
    test_159 = {
        'hostname': '10.0.0.159',
        'port': 22,
        'username': 'www',
        'password': '123456789'
    }
    test_189 = {
        'hostname': '10.0.0.189',
        'port': 22,
        'username': 'www',
        'password': '123456789'
    }
    test_188 = {
        'hostname': '10.0.0.188',
        'port': 22,
        'username': 'www',
        'password': '123456789'
    }
    test_160 = {
        'hostname': '10.0.0.160',
        'port': 22,
        'username': 'www',
        'password': '123456789'
    }
    uat_2221 = {
        'hostname': '10.0.15.21',
        'port': 2221,
        'username': 'www',
        'password': '123456789'
    }
    uat_2222 = {
        'hostname': '10.0.15.21',
        'port': 2222,
        'username': 'www',
        'password': '123456789'
    }


class ServiceDistributeConfig:
    uat_2222 = [
        'ec-warehouse-base-service',
        'ec-warehouse-delivery-service',
        'ec-warehouse-receipt-service',
        'ec-warehouse-transfer-service',
        'ec-stockoperation-service',
        'ec-stockoperation-api',
        'ec-wms-api',
        'ec-pwms-api',
        'ec-supply-platform-service'
    ]
    uat_2221 = [
        'ec-gateway',
        'ec-authorization-service',
        'ec-ums-api',
        'ec-base',
        'ec-pms',
        'ec-bpms-service',
        'ec-bpms-api',
        'ec-pipeline-pms',
        'ec-download',
        'ec-order-service',
        'ec-oms',
        'ec-oms-api',
        'ec-scm-service',
        'ec-scm-api',
        'ec-supplier-api',
        'ec-ims-service',
        'ec-spms-api',
        'ec-spms-service'
    ]
    test_159 = [
        'ec-eta',
        'ec-fms-api',
        'ec-fms-service',
        'ec-ims-service',
        'ec-report',
        'ec-wms-api'
    ]
    test_160 = [
        'ec-gateway',
        'ec-authorization-service',
        'ec-ums-api',
        'ec-base',
        'ec-pms',
        'ec-bpms-service',
        'ec-bpms-api',
        'ec-pipeline-pms',
        'ec-download',
        'ec-order-service',
        'ec-oms-api',
        'ec-scm-service',
        'ec-scm-api',
        'ec-supplier-api',
        'ec-spms-api',
        'ec-spms-service',
        'ec-warehouse-base-service',
        'ec-warehouse-delivery-service',
        'ec-warehouse-receipt-service',
        'ec-warehouse-transfer-service',
        'ec-stockoperation-service',
        'ec-pwms-api',
        'ec-supply-platform-service'
    ]
    test_189 = [
        'ec-gateway',
        'ec-fms-service',
        'ec-fms-api',
        'ec-eta',
        'ec-pms',
        'ec-bpms-service',
        'ec-bpms-api',
        'ec-pipeline-pms',
        'ec-download',
        'ec-order-service',
        'ec-ims-service',
        'ec-oms-api',
        'ec-spms-service',
        'ec-spms-api',
        'ec-warehouse-base-service',
        'ec-warehouse-delivery-service',
        'ec-warehouse-receipt-service',
        'ec-warehouse-transfer-service',
        'ec-stockoperation-service',
        'ec-supply-platform-service',
        'ec-report',
        'ec-pwms-api',
        'ec-wms-api'
    ]
    test_188 = [
        'ec-authorization-service',
        'ec-ums-api',
        'ec-base',
        'ec-scm-service',
        'ec-scm-api'
    ]
