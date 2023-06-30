import random
from robots.robot import AppRobot
from dbo.fms_dbo import FMSDBOperator
from dbo.wms_dbo import WMSDBOperator
from copy import deepcopy
from utils.log_handler import logger as log
from utils.random_code import RandomCode
from utils.time_handler import HumanDateTime
from config.third_party_api_configs import fms_api_config


class FMSAppRobot(AppRobot):

    def __init__(self):
        self.dbo = FMSDBOperator
        super().__init__()

    def get_servicer_list(self):
        """
        查询服务商列表
        """
        content = deepcopy(
            fms_api_config.BaseApi.ProviderList.get_attributes()
        )
        res = self.call_api(**content)

        if not res:
            return []

        return res.get("data")

    def get_provider_channel_list(self, provider_code):
        """
        查询服务商下的渠道列表
        :param provider_code: 服务商编码
        """
        content = deepcopy(
            fms_api_config.BaseApi.ChannelListByProvider.get_attributes()
        )
        content["data"]["serviceCode"] = provider_code

        res = self.call_api(**content)

        if not res:
            return []

        return res.get("data")

    def get_fee_item_list(self):
        """
        查询 费用项 列表
        """
        content = deepcopy(
            fms_api_config.FeeItemApi.FeeItemList.get_attributes()
        )
        res = self.call_api(**content)

        return [] if not res.get("data") else res.get("data")

    def save_not_sea_expect_fee_item(self, **param):
        """
        保存 非海运 预估费用项
        :param param: ExpectFeeItemApi.NotSeaExpectFeeItemSave.data
        """
        content = deepcopy(
            fms_api_config.ExpectFeeItemApi.NotSeaExpectFeeItemSave.get_attributes()
        )
        if not param:
            log.error("保存费用项参数不能为空")
            return None

        content["data"].update(**param)

        return self.call_api(**content)

    def get_expect_fee_item_page(self, **param):
        """
        查询 预估费用项 列表，默认分页条数 10
        :param param: ExpectFeeItemApi.ExpectFeeItemPage.data
        """
        content = deepcopy(
            fms_api_config.ExpectFeeItemApi.ExpectFeeItemPage.get_attributes()
        )

        if param:
            content["data"].update(**param)

        res = self.call_api(**content)

        return [] if not res.get("data") else res.get("data")

    def auto_save_expect_fee_item(self, fee_type: int, num: int = 1):
        """
        创建预估费用项
        """
        result_ids = []
        sea_type = fms_api_config.FmsEnum.TransactionType.SEA.value.get("value")
        fee_list = self.get_fee_item_list()

        if not fee_list:
            raise Exception("查询不到费用项记录")

        servicer_list = self.get_servicer_list()
        if not servicer_list:
            raise Exception("查询不到服务商数据")

        servicer_code = random.choice(servicer_list).get("code")
        channel_list = self.get_provider_channel_list(
            servicer_code
        )
        if not channel_list:
            raise Exception("查询不到渠道列表")

        tdo_codes = WMSDBOperator().get_delivery_order_code_list(limit=10)
        delivery_nos = RandomCode("YD-", 8).generate(num)

        # 创建 海运单 预估费用项
        if fee_type == sea_type:
            for i in range(num):
                fee_item = random.choice(fee_list)
                pass
            # todo

            return result_ids

        # 创建 非海运单 预估费用项
        for i in range(num):
            fee_item = random.choice(fee_list)
            tdo_code = random.choice(tdo_codes)
            data = {
                "deliveryNo": delivery_nos[i],
                "outStockNo": tdo_code.get("delivery_order_code"),
                "servicer": servicer_code,
                "transportType": random.choice(
                    [
                        item.value.get('value')
                        for item in fms_api_config.FmsEnum.TransportType
                    ]
                ),
                "transactionType": random.choice(
                    [
                        item.value.get("value")
                        for item in fms_api_config.FmsEnum.TransactionType
                        if item.name != "SEA"
                    ]
                ),
                "goodsAmount": random.randint(100, 800),
                "salesAmount": random.randint(100, 800),
                "salesAmountCurrency": "USD",
                "declareCustomsAmount": 300,
                "declareCustomsAmountCurrency": "USD",
                "chargedWeightKg": 5.5,
                "shippingPlace": "国内",
                "destination": "国外",
                "provinceCode": "T001",
                "postCode": "10086",
                "channel": random.choice(channel_list).get("code"),
                "shippingTime": HumanDateTime().sub(days=-20).human_time("%Y-%m-%d"),
                "chargedWeight": 5.5,
                "chargedWeightUnit": "kg",
                "expectFeeItemDetails": [
                    {
                        "feeItemName": fee_item.get("feeItemName"),
                        "expectAmount": round(random.uniform(30, 200), 2),
                        "expectAmountCurrency": "USD"
                    }
                ],
                "expectFeeItemPackageDetails": [
                    {
                        "packageNo": RandomCode("BG-", 8).generate_one(),
                        "length": 10,
                        "width": 10,
                        "high": 10,
                        "weight": 5
                    }
                ]
            }
            self.save_not_sea_expect_fee_item(**data)










