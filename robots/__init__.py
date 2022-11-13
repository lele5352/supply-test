from urllib.parse import urljoin
import requests
import time
import json

import config
from utils.rsa_handler import encrypt_data
from dbo.ums_dbo import UMSDBOperator
from config.third_party_api_configs.ums_api_config import UMSApiConfig
from config import user
from copy import deepcopy


def login():
    """
    根据配置的系统用户登陆，取得请求头
    """
    key_content = deepcopy(UMSApiConfig.GetPublicKey.get_attributes())
    login_content = deepcopy(UMSApiConfig.Login.get_attributes())
    prefix = config.env_prefix_config.get("app")
    # 先获取公钥
    url = urljoin(prefix, key_content['uri_path'])
    params = {'t': int(time.time() * 1000)}
    res = requests.get(url, params=params).json()
    # 获取到公钥之后拼装begin和end返回
    key = res['data']
    begin = '-----BEGIN PUBLIC KEY-----\n'
    end = '\n-----END PUBLIC KEY-----'
    try:
        public_key = begin + key + end
        # 加密密码并更新密码为加密后的
        encrypt_password = encrypt_data(user['password'], public_key)
        user['password'] = encrypt_password
        data = login_content['data']
        data.update(
            {
                "password": user['password'],
                "username": user['username']
            }
        )
        url = urljoin(prefix, login_content['uri_path'])
        login_res = requests.post(url, json=data).json()
        authorization_str = login_res['data']['tokenHead'] + ' ' + login_res['data']['token']
        headers = {'Content-Type': 'application/json;charset=UTF-8', "Authorization": authorization_str}
        return headers
    except Exception as e:
        print('账号登录失败！', e)
        return None


def get_service_headers():
    username = user['username']
    user_id = UMSDBOperator.query_sys_user(username).get('id')
    service_header = {"user": json.dumps({"username": username, 'user_id': user_id}), "serviceName": "ec-scm-service"}
    return service_header


app_headers = login()
service_headers = get_service_headers()
