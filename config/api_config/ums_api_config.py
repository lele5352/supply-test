ums_api_config = {
    "get_public_key": {
        "uri_path": "/api/ec-ums-api/user/rsa/publicKey",
        "method": "get",
        "data": {'t': 0}
    },
    "login": {
        "uri_path": "/api/ec-ums-api/user/login",
        "method": "post",
        "data": {
            "code": "dw2m",
            "grant_type": "password",
            "password": '123456',
            "randomStr": "",
            "scope": "server",
            "username": 'xuhongwei@popicorns.com',
        }
    }
}
