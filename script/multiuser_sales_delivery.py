import threading
from robot_run.run_delivery import RunDelivery, WMSAppRobot


def perform_delivery(user_data):
    user_info = {
        "username": user_data.get("user_name"),
        "password": user_data.get("pwd")
    }
    order_code = user_data.get("order_code")
    warehouse_id = user_data.get("warehouse")

    wms = WMSAppRobot(**user_info)
    rd = RunDelivery(wms)
    rd.run_delivery(order_code, warehouse_id)


def main():
    data_list = [
        {
            "user_name": "cj@popicorns.com",
            "pwd": "A123456",
            "order_code": "PRE-CK2308230033",
            "warehouse": 532
        },
        {
            "user_name": "linzhongjie@popicorns.com",
            "pwd": "Aa123456",
            "order_code": "PRE-CK2308230040",
            "warehouse": 532
        }
    ]

    threads = [threading.Thread(target=perform_delivery, args=(data,)) for data in data_list]
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()


if __name__ == '__main__':
    main()
