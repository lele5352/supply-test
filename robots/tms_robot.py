import json
from copy import deepcopy
from config.third_party_api_configs.tms_api_config \
    import TMSApiConfig, UnitType, TransportType, AddressType
from robots.robot import AppRobot, ServiceRobot
from dbo.tms_dbo import TMSBaseDBOperator
from utils.tms_cal_items import TMSCalcItems
from utils.unit_change_handler import UnitChange
from utils.time_handler import HumanDateTime
from utils.log_handler import logger
from utils.check_util import check_isinstance
import uuid


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


class HomaryTMS(ServiceRobot):
    """
    爆米物流应用

    示例：
        初始化类
            >> t = HomaryTMS()

        生成参数
            >> express_trial_body = t.build_trial_body(TransportType.EXPRESS, 170, 'US') # 生成快递试算参数
            >> track_trial_body = t.build_trial_body(TransportType.TRACK, 170, 'US') # 生成卡车试算参数
            >> express_order_body = t.build_order_body(TransportType.EXPRESS, 170, 'US') # 生成快递下单参数
            >> track_order_body = t.build_order_body(TransportType.TRACK, 170, 'US') # 生成卡车下单参数

        调用试算
            >> t.do_trial(express_trial_body)  # 执行快递试算
            >> t.do_trial(track_trial_body)  # 执行卡车试算

        调用下单
            >> t.do_order(express_order_body)  # 执行快递下单
            >> t.do_order(track_order_body)  # 执行卡车下单

    """

    def __init__(self):
        super().__init__('homary_tms')

    @staticmethod
    def build_address(body, address_id, trial_country, address_type):
        """
        组装地址参数
        """
        address_data = TMSApiConfig.TrialAddress.get_attributes()
        try:
            trial_address = address_data[trial_country]
        except KeyError:
            raise AssertionError(f'{trial_country} 无对应试算地址配置')

        body["address"] = trial_address
        body["address"]["receiveAddressId"] = address_id
        body["address"]["addressType"] = address_type.value

    @staticmethod
    def build_packages(body, transport_type, build_type=1, **kwargs):
        """
        组装包裹信息
        Args:
            body: 参数字典
            transport_type: 运输方式
            build_type: 调用类型 1 试算 2 下单

        Keyword Args:
            prod_name: 货物名称：传入仓库sku用于获取申报价
            weight: 重量，定义包裹/托盘 的重量
            length: 长，定义包裹/托盘 的长
            width: 宽，定义包裹/托盘 的宽
            height: 高，定义包裹/托盘 的高
            category: 货物品类，卡车托盘品类，不传时默认为空
            goods_desc: 货物描述
            channel_id: 渠道id，用于指定渠道下单
        """
        if kwargs.get('channel_id'):
            if not isinstance(kwargs.get('channel_id'), int):
                raise AssertionError("渠道id 类型必须为 int")

        channel_id = kwargs.get('channel_id', None)

        # 初始化货物规格：包裹长宽高重量/托盘长宽高重量
        good_specs = {
            "weight": kwargs.get("weight", 3.9),
            "length": kwargs.get("length", 29.9),
            "height": kwargs.get("height", 29.9),
            "width": kwargs.get("width", 31.9)
        }
        # 货物信息
        goods = [
            {
                "prodName": kwargs.get("prod_name", "J04CJ000483BA02"),
                "qty": 1
            }
        ]
        # 填充货物规格属性
        goods[0].update(good_specs)

        pack_key = 'expressPacks'

        # 卡车下单，托盘信息是 dict 类型，快递试算/快递下单/卡车试算，都是 list
        if transport_type.value == TransportType.TRACK.value and build_type != 1:
            pack_key = 'carTray'
            body[pack_key] = {
                "trays": [
                    {
                        "prodName": "测试托盘",
                        "qty": 1,
                        "category": kwargs.get("category"),
                        "goodsDesc": kwargs.get("goods_desc"),
                        'goodsDetails': goods
                    }
                ]
            }
            body[pack_key]['trays'][0].update(good_specs)

            if channel_id:
                body[pack_key]["channelId"] = channel_id

        else:
            # 这堆 if else 为了兼容 卡车/快递 的接口字段命名和类型不一致...
            if transport_type.value == TransportType.TRACK.value:
                pack_key = 'carTrayDetails'

            body[pack_key] = [
                {
                    "goodsDetails": goods,
                    "category": kwargs.get("category")
                }
            ]
            body[pack_key][0].update(good_specs)

            if transport_type.value != TransportType.TRACK.value:
                body[pack_key][0]['packName'] = '测试包裹'
            else:
                body[pack_key][0]['prodName'] = '测试托盘'
                body[pack_key][0]['qty'] = 1

            if channel_id:
                for _ in body[pack_key]:
                    _['channelId'] = kwargs.get('channel_id')

    @staticmethod
    def build_pick_info(body, **kwargs):
        """
        组装提货信息
        Args:
            body: 参数字典

        Keyword Args:
            pick_date: 提货日期，未传时，默认为 8天后 (fedex快递未来提货日期不能超过10天，卡车不能超过5天)
            min_pick: 最小提货时间
            max_pick: 最大提货时间
            min_delivery: 最小送货时间
            max_delivery: 最大送货时间
            insure_category: 投保类目
            insure_price: 投保金额
            insure_currency: 投保币种
        """
        body["pickInfo"] = {
            "pickDate": kwargs.get('pick_date', HumanDateTime().add(days=8).human_time()),
            "minPickTime": kwargs.get('min_pick', '08:00'),
            "maxPickTime": kwargs.get('max_pick', '17:00'),
            "minDeliveryTime": kwargs.get('min_delivery', '08:00'),
            "maxDeliveryTime": kwargs.get('max_delivery', '17:00'),
            "insureProdCategory": kwargs.get('insure_category'),
            "insurePrice": kwargs.get('insure_price'),
            "insureGoodsCurrency": kwargs.get('insure_currency')
        }

    def build_trial_body(self, transport_type: TransportType,
                         address_id: int, trial_country: str,
                         address_type: AddressType = None,
                         unit: UnitType = None,
                         **kwargs):
        """
        试算参数组装
        Args:
            transport_type: 运输方式 1-快递；2-卡车
            address_id: 仓库地址id
            trial_country: 试算地址区域 US 美国 DE 德国 FR 法国
            address_type: 地址类型
            unit: 单位  10-国标（kg/cm）；20-英制（lb/inch），默认 国标

        Keyword Args:
            channel_id: 渠道id，类型为 tuple or int
            forward_flag: 正向订单标志 true:正向 false:逆向
            prod_name: 货物名称：传入仓库sku用于获取申报价
            weight: 重量
            length: 长
            width: 宽
            height: 高
            category: 货物品类

        """
        # 未传入地址类型时，使用 商业地址带月台
        if not address_type:
            address_type = AddressType.BUSINESS_ADDRESS_P
        if not unit:
            unit = UnitType.NATIONAL

        check_isinstance(address_type, AddressType, 'address_type')
        check_isinstance(transport_type, TransportType, 'transport_type')
        check_isinstance(unit, UnitType, 'unit')

        req = {
            "transportType": transport_type.value,
            "unit": unit.value,
            "forwardFlag": kwargs.get('forward_flag', False),
            "channelIds": []
        }

        channels = kwargs.get('channel_id')
        if isinstance(channels, tuple):
            req["channelIds"].extend(list(channels))
        elif isinstance(channels, int):
            req["channelIds"].append(channels)

        self.build_address(req, address_id, trial_country, address_type)
        self.build_packages(req, transport_type, **kwargs)

        return req

    def build_order_body(self, transport_type: TransportType,
                         address_id: int, trial_country: str,
                         address_type: AddressType = None,
                         unit: UnitType = None,
                         **kwargs):
        """
        下单参数组装
        Args:
            transport_type: 运输方式 TransportType 枚举 1-快递；2-卡车
            address_id: 仓库地址id
            trial_country: 试算地址区域 US 美国 DE 德国 FR 法国
            address_type: 地址类型：AddressType枚举，未传时默认为 商业地址
            unit: 单位  10-国标（kg/cm）；20-英制（lb/inch），默认 国标

        Keyword Args:
            channel_id: 渠道id，用于指定渠道下单
            forward_flag: 正向订单标志 true:正向 false:逆向
            pick_date: 提货日期，不传时取默认时间
            source_pack_code: 来源包裹号
            prod_name: 货物名称：传入仓库sku用于获取申报价
            weight: 重量
            length: 长
            width: 宽
            height: 高
            category: 货物品类
            min_pick: 最小提货时间
            max_pick: 最大提货时间
            min_delivery: 最小送货时间
            max_delivery: 最大送货时间
            insure_category: 投保类目
            insure_price: 投保金额
            insure_currency: 投保币种
        """

        # 未传入地址类型时，使用 商业地址带月台
        if not address_type:
            address_type = AddressType.BUSINESS_ADDRESS_P
        if not unit:
            unit = UnitType.NATIONAL

        check_isinstance(address_type, AddressType, 'address_type')
        check_isinstance(transport_type, TransportType, 'transport_type')
        check_isinstance(unit, UnitType, 'unit')

        req = {
            "idempotentId": str(uuid.uuid4()),
            "transportType": transport_type.value,
            "unit": unit.value,
            "forwardFlag": kwargs.get('forward_flag', False),
            "sourceOrderCode": kwargs.get('source_order_code', '自动测试单'),
            "assignChannelFlag": False
        }

        # 如果有传渠道id，则认定为 指定渠道下单
        if kwargs.get('channel_id'):
            req["assignChannelFlag"] = True

        self.build_address(req, address_id, trial_country, address_type)
        self.build_packages(req, transport_type, build_type=2, **kwargs)
        self.build_pick_info(req, **kwargs)

        return req

    def do_trial(self, req_data):
        """
        试算同步接口请求
        yapi 接口文档   https://yapi.popicorns.com/project/437/interface/api/38305
        :param req_data: 请求参数体
        """
        content = deepcopy(TMSApiConfig.SyncTrial.get_attributes())
        content["data"] = req_data

        return self.call_api(**content)

    def do_order(self, req_data):
        """
        下单同步接口请求
        yapi 接口文档   https://yapi.popicorns.com/project/437/interface/api/38308
        :param req_data: 请求参数体
        """
        content = deepcopy(TMSApiConfig.SyncOrder.get_attributes())
        content["data"] = req_data

        return self.call_api(**content)
