import time
import json
import requests
from urllib.parse import urljoin

from utils.rsa_handler import encrypt_data
from config import user
from utils.mysql_handler import MysqlHandler
from config import app_prefix, mysql_info


def get_ims_headers():
    headers = {
        "serviceName": "ec-warehouse-delivery-service"
    }
    return headers


def get_app_headers():
    authorization = ums_login()
    headers = {'Content-Type': 'application/json;charset=UTF-8', "Authorization": authorization}
    return headers


def get_service_headers():
    db = MysqlHandler(mysql_info, 'supply_auth')
    username = user['username']
    user_id = db.get_one("select id from sys_user where username ='%s'" % username)
    header = {"user": json.dumps({"username": username, 'user_id': user_id['id']})}
    return header


def get_public_key():
    timestamp = int(time.time() * 1000)

    headers = {'Content-Type': 'application/json;charset=UTF-8'}

    uri = "/api/ec-ums-api/user/rsa/publicKey"
    url = urljoin(app_prefix, uri)

    data = {'t': timestamp}

    res = requests.get(url, headers=headers, json=data)
    # 获取到公钥之后拼装begin和end返回
    key = res.json()['data']
    begin = '-----BEGIN PUBLIC KEY-----\n'
    end = '\n-----END PUBLIC KEY-----'
    try:
        public_key = begin + key + end
        return public_key
    except TypeError:
        return


def ums_login(specific_user=False, username='', password=''):
    """
    :param username: 用户名，仅指定用户账号时填写
    :param password: 密码，仅指定用户账号时填写
    :param specific_user: 是否指定用户登录
    :return: authorization_str: 登录完拼装出来的鉴权字符串
    """
    # 先获取公钥
    public_key = get_public_key()
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

    headers = {'Content-Type': 'application/json;charset=UTF-8'}

    uri = "/api/ec-ums-api/user/login"
    url = urljoin(app_prefix, uri)

    data = {
        "code": "dw2m",
        "grant_type": "password",
        "password": user['password'],
        "randomStr": "",
        "scope": "server",
        "username": user['username'],
    }
    try:
        res = requests.post(url, headers=headers, json=data).json()
        authorization_str = res['data']['tokenHead'] + ' ' + res['data']['token']
        return authorization_str
    except:
        print('账号登录失败！')
        return None
