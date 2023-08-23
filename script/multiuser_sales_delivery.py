import asyncio
from robot_run.run_delivery import RunDelivery, WMSAppRobot


async def perform_delivery(user_data):

    user_info = {
        "username": user_data.get("user_name"),
        "password": user_data.get("pwd")
    }
    order_code = user_data.get("order_code")
    warehouse_id = user_data.get("warehouse")

    wms = WMSAppRobot(user_info)
    rd = RunDelivery(wms)
    rd.run_delivery(order_code, warehouse_id)


async def main():

    data_list = [
        {
            "user_name": "cj@popicorns.com",
            "pwd": "A123456",
            "order_code": "PRE-CK2308230021",
            "warehouse": 532
        },
        {
            "user_name": "linzhongjie@popicorns.com",
            "pwd": "Aa123456",
            "order_code": "PRE-CK2308230020",
            "warehouse": 532
        }
    ]

    tasks = [perform_delivery(data) for data in data_list]
    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
