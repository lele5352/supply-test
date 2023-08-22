import asyncio
from robots import login, switch_warehouse
import aiohttp


def login_and_switch(username, password, warehouse_id):

    login_req = {
        "username": username,
        "password": password
    }

    # 登录，并切换到用户指定仓库
    headers = login(login_req)
    rs = switch_warehouse(warehouse_id, headers)
    if rs == 200:
        return headers

    return None


async def perform_stock_assign(session, host, user_data):

    username = user_data.get('user_name')
    password = user_data.get('pwd')
    order_code = user_data.get('order_code')
    req_url = f"{host}/api/ec-wms-api/delivery-order/stock-assign/v2"
    headers = login_and_switch(username, password, user_data["warehouse"])
    if not headers:
        raise ValueError("登录/切换仓库失败")

    # 请求参数组装
    payload = {
        "deliveryOrderCodes": [order_code]
    }

    async with session.post(req_url, headers=headers, json=payload) as response:
        result = await response.json()
        print(f"User {username} - Order Code {order_code} - Result: {result}")


async def main():
    host_url = "https://test-scms.popicorns.com"
    data_list = [
        {
            "user_name": "cj@popicorns.com",
            "pwd": "A123456",
            "order_code": "PRE-CK2308220025",
            "warehouse": 532
        },
        {
            "user_name": "linzhongjie@popicorns.com",
            "pwd": "Aa123456",
            "order_code": "PRE-CK2308220001",
            "warehouse": 532
        }
    ]

    async with aiohttp.ClientSession() as session:
        tasks = [perform_stock_assign(session, host_url, data) for data in data_list]
        await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
