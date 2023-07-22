import random
import time
from dbo.oms_dbo import OMSDBOperator
from models.eta_model import *
from models.oms_model import OmsLogisticsCleanInfo
from playhouse.shortcuts import model_to_dict

from utils.random_code import get_random_times


class ETADBOperator:
    @classmethod
    def load_data(cls, data_count=1, country_code='US', postal_code='9999', transport_type=None, exception_status=None,
                  first_appointment_period=('2023-07-05 00:00:00', '2023-07-21 00:00:00'),
                  first_contact_period=('2023-07-05 00:00:00', '2023-07-21 00:00:00'),
                  delivered_period=('2023-07-05 00:00:00', '2023-07-21 00:00:00'),
                  issue_time_period=('2023-07-01 00:00:00', '2023-07-10 00:00:00'),
                  re_check_time_period=('2023-07-01 00:00:00', '2023-07-03 00:00:00'),
                  warehouse_code='LA01', virtual_warehouse_code='OMS_USLA01'):
        """
        :param int data_count: 生成的数据条数
        :param str country_code: 国家编码
        :param str postal_code: 邮编
        :param str virtual_warehouse_code: 共享仓编码
        :param str warehouse_code: 实际仓编码
        :param tuple(day,day) first_appointment_period: 首次预约时间
        :param tuple(day,day) first_contact_period: 首次联系时间
        :param tuple(day,day) delivered_period: 妥投时间
        :param transport_type: 1 快递 2 卡车
        :param tuple(day,day) issue_time_period: 下发时间
        :param tuple(day,day) re_check_time_period: 复核时间
        :param int exception_status: 异常处理状态 默认1 正常 2 待处理 3 已跳过 4 已处理
        """
        # 自动排序时间段字段
        if exception_status not in (1, 2, 4, None):
            raise Exception('异常处理状态不合法')
        country_info = cls.get_country_info()
        warehouse_info = cls.get_warehouse_info()
        virtual_warehouse_info = OMSDBOperator.get_virtual_warehouse_info()
        data_source = []
        for i in range(0, data_count):
            # 确定下发和复核时间
            issue_time = get_random_times(*issue_time_period)
            re_check_time = get_random_times(*re_check_time_period)
            if issue_time < re_check_time:
                # print('recheck time is later than issue time')
                continue
            # 确定异常状态和发货方式
            exception_status_new = exception_status or random.choice([1, 2, 4])
            transport_type_new = transport_type or random.choice([1, 2])
            # 计算清洗后妥投时间
            delivered_at = get_random_times(*delivered_period)
            if transport_type == 2 or exception_status in (1, 4):
                first_appointment_at = get_random_times(*first_appointment_period)
                first_contact_at = get_random_times(*first_contact_period)
                clean_delivered_at = min(first_contact_at, first_appointment_at, delivered_at)
            else:
                first_appointment_at = None
                first_contact_at = None
                clean_delivered_at = delivered_at
            if clean_delivered_at < issue_time:
                # print('issue time is later than clean delivery time')
                continue
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
                    "clean_delivered_at": clean_delivered_at,
                    "first_appointment_at": first_appointment_at,
                    "first_contact_at": first_contact_at,
                    "delivery_time": delivered_at,  # 收件时间
                    "delivered_at": delivered_at,  # 妥投时间
                    "channel_code": 'DHL.HKA.YFH',  # 渠道编码 182 快递 181 卡车
                    "transport_type": transport_type_new,  # 1 快递 2 卡车
                    "issue_time": issue_time,  # 下发时间
                    "re_check_time": re_check_time,  # 复核时间
                    "exception_status": exception_status_new,  # 异常处理状态 默认1 正常 2 待处理 3 已跳过 4 已处理
                    "create_user": 1,  # 创建人id
                    "update_user": 1,  # 更新人id
                    "create_user_name": 'load_data_test_user',  # 创建人名称(昵称)
                    "update_user_name": 'load_data_test_user',  # 更新人名称(昵称)
                }
            )
        else:
            # print('=== load {} records ==='.format(len(data_source)))   # debug
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
    ETADBOperator.load_data(data_count=100)
    # ETADBOperator.load_data(data_count=1, country_code='UK', postal_code='100001')
