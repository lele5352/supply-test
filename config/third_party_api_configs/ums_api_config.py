from config.third_party_api_configs import ApiConfig


class UMSApiConfig:
    class GetPublicKey(ApiConfig):
        uri_path = "/api/ec-ums-api/user/rsa/publicKey"
        method = "get",
        data = {'t': 0}

    class Login(ApiConfig):
        uri_path = "/api/ec-ums-api/user/login"
        method = "post",
        data = {
            "code": "dw2m",
            "grant_type": "password",
            "password": '123456',
            "randomStr": "",
            "scope": "server",
            "username": 'xuhongwei@popicorns.com',
        }

    class UserInfo(ApiConfig):
        uri_path = "/api/ec-ums-api/user/info"
        method = "get"
        data = {"t": 0}

