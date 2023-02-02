from robots.robot import AppRobot
from dbo.fms_dbo import FMSDBOperator
from copy import deepcopy
from utils.log_handler import logger as log
from config.third_party_api_configs import fms_api_config


class FMSAppRobot(AppRobot):

    def __init__(self):
        self.dbo = FMSDBOperator
        super().__init__()

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












