from urllib.parse import urljoin
import requests
import time
import json

import config
from utils.rsa_handler import encrypt_data
from dbo.ums_dbo import UMSDBOperator
from config.third_party_api_configs.ums_api_config import UMSApiConfig
from config.third_party_api_configs.wms_api_config import BaseApiConfig
from config import user as default_user
from copy import deepcopy

# 设置域名
prefix = config.env_prefix_config.get("app")


def login(login_user=None):
    """
    根据配置的系统用户登陆，取得请求头
    :param login_user: 传入的登录用户数据，dict 类型
        例子：
        {
            'username': 'xxx@popicorns.com',
            'password': '123456'
        }
    """
    user = login_user or default_user
    key_content = deepcopy(UMSApiConfig.GetPublicKey.get_attributes())
    login_content = deepcopy(UMSApiConfig.Login.get_attributes())
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
    username = default_user['username']
    user_id = UMSDBOperator.query_sys_user(username).get('id')
    # 领域接口请求头，默认去掉 gzip 参数值，以兼容不支持http2的微服务
    service_header = {"user": json.dumps({"username": username, 'user_id': user_id}), "serviceName": "ec-scm-service",
                      "Accept-Encoding": "deflate, br"}
    return service_header


app_headers = login()
service_headers = get_service_headers()


def get_switch_perm_id(warehouse_id, headers=None):
    """
    获取 permId
    """
    headers = headers or app_headers
    content = deepcopy(BaseApiConfig.GetSwitchWarehouseList.get_attributes())
    url = urljoin(prefix, content["uri_path"])
    req_body = {"t": int(time.time() * 1000)}

    res = requests.get(url, headers=app_headers, params=req_body).json()

    for perm in res["data"]:
        if perm["dataId"] == int(warehouse_id):
            return perm["id"]

    return None


def switch_warehouse(warehouse_id, headers=None):
    """
    切换仓库
    """
    headers = headers or app_headers
    content = deepcopy(BaseApiConfig.SwitchDefaultWarehouse.get_attributes())
    url = urljoin(prefix, content["uri_path"])
    perm_id = get_switch_perm_id(warehouse_id)
    if not perm_id:
        raise ValueError("切换仓库失败，查询不到对应的permId")

    req_body = {"dataPermId": perm_id}
    res = requests.put(url, json=req_body, headers=app_headers).json()

    return res.get("code")

