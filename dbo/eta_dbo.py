import time
from dbo.oms_dbo import OMSDBOperator
from models.eta_model import *
from models.oms_model import OmsLogisticsCleanInfo
from playhouse.shortcuts import model_to_dict

from utils.random_code import get_random_times


class ETADBOperator:
    @classmethod
    def load_data(cls, data_count=1, country_code='US', postal_code='999001', transport_type=1, exception_status=2,
                  delivery_time=('2023-07-02 00:00:00', '2023-07-21 00:00:00'),
                  delivered_at=('2023-07-02 00:00:00', '2023-07-21 00:00:00'),
                  issue_time=('2023-03-01 00:00:00', '2023-07-01 00:00:00'),
                  re_check_time=('2023-03-01 00:00:00', '2023-07-01 00:00:00'),
                  warehouse_code='LA01', virtual_warehouse_code='OMS_USLA01'):
        """
        :param int data_count: 生成的数据条数
        :param str country_code: 国家编码
        :param str postal_code: 邮编
        :param str virtual_warehouse_code: 共享仓编码
        :param str warehouse_code: 实际仓编码
        :param tuple(day,day) delivery_time: 收件时间
        :param tuple(day,day) delivered_at: 妥投时间
        :param transport_type: 1 快递 2 卡车
        :param tuple(day,day) issue_time: 下发时间
        :param tuple(day,day) re_check_time: 复核时间
        :param int exception_status: 异常处理状态 默认1 正常 2 待处理 3 已跳过 4 已处理
        """
        # 自动排序时间段字段
        delivery_time = sorted(delivery_time)
        delivered_at = sorted(delivered_at)
        issue_time = sorted(issue_time)
        re_check_time = sorted(re_check_time)
        # 过滤不符合预期的数据
        if exception_status == 3 and delivery_time[1] - issue_time[0] > 15:  # todo: 确认清洗表是否
            raise Exception('已跳过的异常TMS运单，妥投时长超过15天自动过滤')
        if delivered_at[0] < issue_time[1]:
            raise Exception("妥投时间大于下发时间不合理")
        # 获取站点和仓库信息
        country_info = cls.get_country_info()
        warehouse_info = cls.get_warehouse_info()
        virtual_warehouse_info = OMSDBOperator.get_virtual_warehouse_info()
        data_source = []
        for i in range(0, data_count):
            data_source.append(
                {
                    "logistics_no": "FAKE_DATA_{}_{}".format(i, time.time_ns()),  # 运单号
                    "delivery_no": "FAKE_DATA_{}_{}".format(i, time.time_ns()),  # 出库单号
                    "country_code": country_code if country_code != 'UK' else 'GB',  # 国家编码
                    "country_name": country_info[country_code if country_code != 'UK' else 'GB'],  # 国家名称
                    "site_code": country_code,  # 站点
                    "postal_code": postal_code,  # 邮编
                    "virtual_warehouse_code": virtual_warehouse_code,  # 共享仓编码
                    "virtual_warehouse_name": virtual_warehouse_info[virtual_warehouse_code],  # 共享仓名称
                    "warehouse_code": warehouse_code,  # 实际仓编码
                    "warehouse_id": warehouse_info[warehouse_code][0],  # 实际仓id
                    "warehouse_name": warehouse_info[warehouse_code][1],  # 实际仓名称
                    "delivery_time": get_random_times(*delivery_time),  # 收件时间
                    "delivered_at": get_random_times(*delivered_at),  # 妥投时间
                    "channel_code": {1: 182, 2: 181}[transport_type],  # 渠道编码 182 快递 181 卡车
                    "transport_type": transport_type,  # 1 快递 2 卡车
                    "issue_time": get_random_times(*issue_time),  # 下发时间
                    "re_check_time": get_random_times(*re_check_time),  # 复核时间
                    "exception_status": exception_status,  # 异常处理状态 默认1 正常 2 待处理 3 已跳过 4 已处理
                    "create_user": 1,  # 创建人id
                    "update_user": 1,  # 更新人id
                    "create_user_name": 'load_data_test_user',  # 创建人名称(昵称)
                    "update_user_name": 'load_data_test_user',  # 更新人名称(昵称)
                }
            )
        OmsLogisticsCleanInfo.insert_many(data_source).execute()

    @classmethod
    def get_country_info(cls):
        items = CountryArea.select().where(CountryArea.level == 0)
        items = {
            model_to_dict(item)['code']: model_to_dict(item)['name']
            for item in items
        }
        return items

    @classmethod
    def get_warehouse_info(cls):
        items = EcWarehouse.select().where(EcWarehouse.warehouse_status == 1)
        items = {
            model_to_dict(item)['warehouse_code']:
                (model_to_dict(item)['warehouse_id'], model_to_dict(item)['warehouse_name'])
            for item in items}
        return items


if __name__ == '__main__':
    # ETADBOperator.load_data(3000)
    ETADBOperator.load_data(1000, country_code='UK', postal_code='10001')
