from urllib.parse import urljoin
import requests
import time
import json

import config
from utils.rsa_handler import encrypt_data
from utils.log_handler import logger as log
from dbo.ums_dbo import UMSDBOperator
from config.third_party_api_configs.ums_api_config import UMSApiConfig
from config import user as default_user
from copy import deepcopy

# 设置域名
app_prefix = config.env_prefix_config.get("app")


def login(user_name, password):
    """
    根据配置的系统用户登陆，取得请求头
    :param user_name
    :param password
    """
    user_name = user_name
    log.info(f"当前登录用户账号：{user_name}，加密前密码：{password}")

    key_content = deepcopy(UMSApiConfig.GetPublicKey.get_attributes())
    login_content = deepcopy(UMSApiConfig.Login.get_attributes())
    # 先获取公钥
    url = urljoin(app_prefix, key_content['uri_path'])
    params = {'t': int(time.time() * 1000)}
    res = requests.get(url, params=params).json()
    # 获取到公钥之后拼装begin和end返回
    key = res['data']
    begin = '-----BEGIN PUBLIC KEY-----\n'
    end = '\n-----END PUBLIC KEY-----'

    public_key = begin + key + end
    # 加密密码并更新密码为加密后的
    encrypt_password = encrypt_data(password, public_key)
    data = login_content['data']
    data.update(
        {
            "password": encrypt_password,
            "username": user_name
        }
    )
    url = urljoin(app_prefix, login_content['uri_path'])

    try:
        login_res = requests.post(url, json=data).json()
        authorization_str = login_res['data']['tokenHead'] + ' ' + login_res['data']['token']
        headers = {'Content-Type': 'application/json;charset=UTF-8', "Authorization": authorization_str}

    except KeyError:
        raise KeyError('账号登录失败！')

    return headers


def get_service_headers():
    username = default_user['username']
    user_id = UMSDBOperator.query_sys_user(username).get('id')
    # 领域接口请求头，默认去掉 gzip 参数值，以兼容不支持http2的微服务
    service_header = {"user": json.dumps({"username": username, 'user_id': user_id}), "serviceName": "ec-scm-service",
                      "Accept-Encoding": "deflate, br"}
    return service_header


# 为了支持多用户，把登录下沉到AppRobot再进行调用
# app_headers = login()

service_headers = get_service_headers()
