import json

from config.sys_config import user
from db_operator.ums_db_operator import UMSDBOperator
from logics import ums_request


class UmsLogics():
    def __init__(self):
        self.ums_request = ums_request

    @classmethod
    def get_service_headers(cls):
        username = user['username']
        user_id = UMSDBOperator.query_sys_user(username).get('id')
        header = {"user": json.dumps({"username": username, 'user_id': user_id})}
        return header

    def get_app_headers(self):
        res = self.ums_request.ums_login()
        authorization_str = res['data']['tokenHead'] + ' ' + res['data']['token']
        headers = {'Content-Type': 'application/json;charset=UTF-8', "Authorization": authorization_str}
        return headers
