import time

from utils.ssh_handler import SSHHandler

server_info = {
    '159': {'hostname': '10.0.0.159',
            'port': 22,
            'username': 'www',
            'password': '123456789'},
    '189': {'hostname': '10.0.0.189',
            'port': 22,
            'username': 'www',
            'password': '123456789'},
    '188': {'hostname': '10.0.0.188',
            'port': 22,
            'username': 'www',
            'password': '123456789'},
    '160':
        {
            'hostname': '10.0.0.160',
            'port': 22,
            'username': 'www',
            'password': '123456789'
        },
    'uat_2221': {
        'hostname': '10.0.15.21',
        'port': 2221,
        'username': 'www',
        'password': '123456789'
    },
    'uat_2222': {
        'hostname': '10.0.15.21',
        'port': 2222,
        'username': 'www',
        'password': '123456789'
    }
}

services = {
    'uat_2222': [
        'ec-warehouse-base-service',
        'ec-warehouse-delivery-service',
        'ec-warehouse-receipt-service',
        'ec-warehouse-transfer-service',
        'ec-stockoperation-service',
        'ec-stockoperation-api',
        'ec-wms-api',
        'ec-pwms-api',
        'ec-supply-platform-service'
    ],
    'uat_2221': [
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
    ],
    '159': [
        'ec-eta',
        'ec-fms-api',
        'ec-fms-service',
        'ec-ims-service',
        'ec-report',
        'ec-wms-api'
    ],
    '160': [
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
        'ec-stockoperation-api',
        'ec-pwms-api',
        'ec-supply-platform-service'
    ],
    '189': [
        'ec-gateway',
        'ec-fms-service',
        'ec-pms',
        'ec-bpms-service',
        'ec-bpms-api',
        'ec-pipeline-pms',
        'ec-download',
        'ec-order-service',
        'ec-ims-service',
        'ec-oms-api',
        'ec-spms-service',
        'ec-warehouse-base-service',
        'ec-warehouse-delivery-service',
        'ec-warehouse-receipt-service',
        'ec-warehouse-transfer-service',
        'ec-stockoperation-service',
        'ec-stockoperation-api',
        'ec-pwms-api'
    ],
    '188': [
        'ec-authorization-service',
        'ec-ums-api',
        'ec-base',
        'ec-scm-service',
        'ec-scm-api'
    ]}


class EnvManager(SSHHandler):
    def __init__(self, server_info, services):
        self.services = services
        super().__init__(**server_info)

    def get_cd_dir_command(self, service_name):
        if service_name in self.services:
            if service_name == 'ec-scm-service':
                cd_dir_command = "cd /data/ec-scm-service/scm-bootstrap/target/app/bin/"
            else:
                cd_dir_command = "cd /data/%s/target/app/bin/" % service_name
            return cd_dir_command
        else:
            return 'Service name error！'

    @classmethod
    def get_shutdown_command(cls):
        shutdown_command = "sh shutdown.sh"
        return shutdown_command

    @classmethod
    def get_startup_command(cls):
        startup_command = "sh startup.sh --spring.profiles.active=pre"
        return startup_command

    def stop_all_service(self, service_name=''):
        try:
            if service_name:
                print(self.exec_cmd(self.get_cd_dir_command(service_name)))
                print(self.exec_cmd(self.get_shutdown_command()))
            else:
                for service in self.services:
                    print(self.exec_cmd(self.get_cd_dir_command(service)))
                    print(self.exec_cmd(self.get_shutdown_command()))
        except Exception as e:
            print('执行失败！%s' % e)
        finally:
            self.ssh_close()

    def restart_service(self, service_name=''):
        try:
            if service_name:
                print(self.exec_cmd(self.get_cd_dir_command(service_name)))
                print(self.exec_cmd(self.get_shutdown_command()))
                time.sleep(3)
                print(self.exec_cmd(self.get_startup_command()))
            else:
                for service in self.services:
                    print(self.exec_cmd(self.get_cd_dir_command(service)))
                    print(self.exec_cmd(self.get_shutdown_command()))
                    time.sleep(3)
                    print(self.exec_cmd(self.get_startup_command()))
        except Exception as e:
            print('执行失败！%s' % e)
        finally:
            self.ssh_close()


if __name__ == '__main__':
    env189 = EnvManager(server_info.get('189'), services.get('189'))
    env188 = EnvManager(server_info.get('188'), services.get('188'))
    # env_uat_2222 = EnvManager160(server_info_2222, services_2222)
    # env_uat_2221 = EnvManager160(server_info_2221, services_2221)

    env188.restart_service()
    # env_uat_2222.restart_service()
    # env_uat_2221.restart_service()
