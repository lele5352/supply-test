import paramiko
import time


class SSHHelper():
    def __init__(self, hostname, port, username, password):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy)
        self.client.connect(hostname=hostname, port=port, username=username, password=password)
        self.channel = self.client.invoke_shell(width=1000, height=100)

    def exec_cmd(self, command):
        self.channel.send(command + '\n')
        time.sleep(1)
        return self.channel.recv(1024).decode()

    def ssh_close(self):
        self.client.close()
