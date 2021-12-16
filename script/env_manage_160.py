import time

from utils.ssh_handler import SSHHandler


class EnvManager160(SSHHandler):
    def __init__(self):
        self.server_info = {
            'hostname': '10.0.0.160',
            'port': 22,
            'username': 'www',
            'password': '123456789'
        }
        super().__init__(**self.server_info)

        self.services = [
            'ec-gateway',
            'es-authorization-service',
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
            'ec-stockoperation-service',
            'ec-warehouse-base-service',
            'ec-warehouse-delivery-service',
            'ec-warehouse-receipt-service',
            'ec-warehouse-transfer-service',
            'ec-stockoperation-api',
            'ec-wms-api',
            'ec-ims-service'
        ]

    def get_cd_dir_command(self, service_name):
        if service_name in self.services:
            if service_name == 'ec-scm-service':
                cd_dir_command = "cd /data/ec-scm-service/scm-bootstrap/target/app/bin/"
            else:
                cd_dir_command = "cd /data/%s/target/app/bin/" % service_name
            return cd_dir_command
        else:
            return 'Service name error！'

    def get_shutdown_command(self):
        shutdown_command = "sh shutdown.sh"
        return shutdown_command

    def get_startup_command(self):
        startup_command = "sh startup.sh --spring.profiles.active=pre"
        return startup_command

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
        except Exception:
            print('执行失败！')
        finally:
            self.ssh_close()


if __name__ == '__main__':
    env160 = EnvManager160()
    env160.restart_service('ec-oms')
