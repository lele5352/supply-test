import time

from utils.ssh_handler import SSHHandler
from config.server_config import ServerInfoConfig, ServiceDistributeConfig


class EnvManager(SSHHandler):
    def __init__(self, info, service):
        self.service = service
        super().__init__(**info)

    def get_cd_dir_command(self, service_name):
        if service_name in self.service:
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
                for service in self.service:
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
                for service in self.service:
                    print(self.exec_cmd(self.get_cd_dir_command(service)))
                    print(self.exec_cmd(self.get_shutdown_command()))
                    time.sleep(3)
                    print(self.exec_cmd(self.get_startup_command()))
        except Exception as e:
            print('执行失败！%s' % e)
        finally:
            self.ssh_close()


if __name__ == '__main__':
    # env_uat_2222 = EnvManager(server_info_2222, services_2222)
    # env_uat_2221 = EnvManager(server_info_2221, services_2221)

    env159 = EnvManager(ServerInfoConfig.test_159, ServiceDistributeConfig.test_159)
    env160 = EnvManager(ServerInfoConfig.test_160, ServiceDistributeConfig.test_160)

    # env188 = EnvManager(ServerInfoConfig.test_188, services.get('188'))
    # env189 = EnvManager(ServerInfoConfig.test_189, services.get('189'))

    env160.restart_service()
    env159.restart_service()

    # env_uat_2222.restart_service()
    # env_uat_2221.restart_service()
