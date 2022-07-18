import time

from utils.rsa_handler import encrypt_data
from utils.request_handler import RequestHandler

from config.api_config.ums_api_config import ums_api_config
from config.sys_config import env_prefix_config, user


class UmsRequest(RequestHandler):
    def __init__(self):
        self.prefix = env_prefix_config.get('app_prefix')
        self.headers = {'Content-Type': 'application/json;charset=UTF-8'}
        super().__init__(self.prefix, self.headers)

    def get_public_key(self):
        timestamp = int(time.time() * 1000)
        ums_api_config['get_public_key']['data'].update({
            't': timestamp
        })
        res = self.send_request(**ums_api_config['get_public_key'])

        # 获取到公钥之后拼装begin和end返回
        key = res['data']
        begin = '-----BEGIN PUBLIC KEY-----\n'
        end = '\n-----END PUBLIC KEY-----'
        try:
            public_key = begin + key + end
            return public_key
        except TypeError:
            return

    def ums_login(self, specific_user=False, username='', password=''):
        """
        :param username: 用户名，仅指定用户账号时填写
        :param password: 密码，仅指定用户账号时填写
        :param specific_user: 是否指定用户登录
        """
        # 先获取公钥
        public_key = self.get_public_key()
        if not public_key:
            return

        # 如果指定账号登录，则用传的账密更新从配置中读取到的账密;否则读取配置中的默认用户的账密
        if specific_user:
            user.update(
                {
                    "username": username,
                    "password": password
                }
            )

        # 加密密码并更新密码为加密后的
        encrypt_password = encrypt_data(user['password'], public_key)
        user['password'] = encrypt_password
        ums_api_config['login']['data'].update(
            {
                "password": user['password'],
                "username": user['username']
            }
        )

        try:
            res = self.send_request(**ums_api_config['login'])
            return res
        except:
            print('账号登录失败！')
            return None


if __name__ == '__main__':
    ums = UmsRequest()
    print(ums.ums_login())