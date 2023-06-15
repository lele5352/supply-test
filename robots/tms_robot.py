import json
from copy import deepcopy
from config.third_party_api_configs.tms_api_config import TMSApiConfig
from robots.robot import AppRobot
from dbo.tms_base_dbo import TMSBaseDBOperator
from utils.tms_cal_items import TMSCalcItems
from utils.unit_change_handler import UnitChange
from utils.log_handler import logger


class TMSRobot(AppRobot):
    def __init__(self):
        self.dbo = TMSBaseDBOperator
        super().__init__()

    def get_express_limit(self, country_code):
        """获取基础库字典快递限制"""
        express_limit_data = self.dbo.get_base_dict("express_limit").get("label_value")
        express_limit = json.loads(express_limit_data)
        express_limit = {key.upper(): value for key, value in express_limit.items()}
        return express_limit.get(country_code)

    def get_package_limit(self, country_code):
        """获取基础库字典包裹限制"""
        package_limit = self.dbo.get_base_dict("package_limit")
        package_limit = {key.upper(): value for key, value in package_limit.items()}
        return package_limit.get(country_code)

    @classmethod
    def is_less_than_limit(cls, limit, goods_limit_item_list):
        max_weight = max([item[0] for item in goods_limit_item_list])
        max_longest_side = max([item[1] for item in goods_limit_item_list])
        max_girth = max([item[2] for item in goods_limit_item_list])
        max_volume_weight = max([item[3] for item in goods_limit_item_list])
        logger.info(
            "max_weight:{},max_longest_side:{},max_girth:{},max_volume_weight:{}".format(
                max_weight, max_longest_side, max_girth, max_volume_weight), sys_out=True)
        if max_weight > limit.get("max_weight"):
            return False
        elif max_longest_side > limit.get("max_length"):
            return False
        elif max_girth > limit.get("gird_size"):
            return False
        elif max_volume_weight > limit.get("throw_heavy"):
            return False
        else:
            return True

    def is_express_valid(self, goods_info, destination_address):
        """判断是否支持走快递,快递限制的数值单位为国际单位，当货物每件计算出来的计量项小于等于快递限制时可走快递"""
        to_country_code = destination_address.get("country")
        express_limit = self.get_express_limit(to_country_code)

        goods_items_list = list()
        for good_info in goods_info.get("goods_list"):
            good_items = TMSCalcItems(*good_info)
            goods_items_list.append(
                (
                    good_items.weight,
                    good_items.longest_side(),
                    good_items.girth(),
                    good_items.volume_weight(express_limit.get("throw_heavy_radio"))
                )
            )

        # 判断货物单位，决定是否需要进行单位换算，快递限制单位为国际单位
        goods_unit = goods_info.get("goods_unit")
        if goods_unit == "imperial":
            unit_changed_goods_items_list = [
                (
                    UnitChange.change(good_items[0], "weight", "yz", "gj"),
                    UnitChange.change(good_items[1], "size", "yz", "gj"),
                    UnitChange.change(good_items[2], "size", "yz", "gj"),
                    round(UnitChange.change(good_items[3], "volume", "yz", "gj"), 2)
                ) for good_items in goods_items_list
            ]
            goods_items_list = unit_changed_goods_items_list
        # 只要货物换算出来的计量项小于快递限制就可发快递
        return self.is_less_than_limit(express_limit, goods_items_list)

    def package_calc(self, goods_info_list, precision):
        temp_result = [0, 0, 0]
        temp_weight = 0
        for length, width, height, weight in goods_info_list:
            sides = [length, width, height]
            sides.sort(reverse=True)
            temp_result = [max(temp_result[0], sides[0]), max(temp_result[1], sides[1]), temp_result[2] + sides[2]]
            temp_result.sort(reverse=True)
            temp_weight += weight
        temp_result.append(round(temp_weight, 6))
        items = TMSCalcItems(temp_result[3], temp_result[0], temp_result[1], temp_result[2])
        grith = items.girth()
        volume_weight = items.volume_weight(precision)
        temp_result.extend([grith, volume_weight])

        return temp_result


if __name__ == '__main__':
    tms = TMSRobot()
    goods_info = {
        "goods_unit": "imperial",
        "goods_list": [
            (18.65, 99.9, 66.6, 55.5),
            (18.66, 99.9, 66.6, 55.5),
            (18.65, 100, 66.6, 55.5),
            (18.65, 99.9, 66.7, 55.5),
            (18.65, 99.9, 66.6, 55.6),

        ]
    }
    destination_info = {
        "country": "US",
        "province": "NJ",
        "city": "Newark",
        "zipcode": "07108"
    }
    print(tms.is_express_valid(goods_info, destination_info))
