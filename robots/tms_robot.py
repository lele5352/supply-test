import json
import random
import uuid
from typing import Tuple

from copy import deepcopy
from config.third_party_api_configs.tms_api_config import *
from robots.robot import AppRobot, ServiceRobot
from dbo.tms_dbo import TMSChannelDBO, TMSBaseDBO, LogisticOrderDBO
from utils.rounding_handler import Rounding
from utils.tms_cal_items import PackageCalcItems
from utils.unit_change_handler import UnitChange
from utils.time_handler import HumanDateTime
from utils.log_handler import logger
from utils.check_util import check_isinstance
from utils.transformer import str_under2hump


class TMSRobot(AppRobot):
    def __init__(self):
        self.dbo = TMSBaseDBO
        super().__init__()

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
    def single_goods_detail(sku_code, **kwargs):
        """
        根据传入的sku编码，组装货物详情
        """
        good_detail = {
            "prodName": sku_code,
            "qty": kwargs.get("qty", 1),
            "weight": kwargs.get("weight", random.uniform(2, 5)),
            "length": kwargs.get("length", random.uniform(10, 30)),
            "width": kwargs.get("width", random.uniform(10, 30)),
            "height": kwargs.get("height", random.uniform(10, 30)),
            "purchasePriceAmount": kwargs.get("purchasePriceAmount", random.uniform(30, 50)),
            "purchasePriceCurrency": kwargs.get("purchasePriceCurrency", "CNY"),
            "salePriceAmount": kwargs.get("salePriceAmount", random.uniform(100, 200)),
            "salePriceCurrency": kwargs.get("purchasePriceCurrency", "CNY"),
            "declareSkuVo": kwargs.get("declareSkuVo", None)
        }

        return good_detail

    def single_express_pack(self, pack_name, sku_code: tuple, **kwargs):
        """
        组装快递参数
        Args:
             pack_name: 包裹名称
             sku_code: tuple类型，sku编码
        """
        express_pack = {
            "packName": pack_name,
            "weight": kwargs.get("weight", random.uniform(2, 5)),
            "length": kwargs.get("length", random.uniform(10, 30)),
            "width": kwargs.get("width", random.uniform(10, 30)),
            "height": kwargs.get("height", random.uniform(10, 30)),
            "goodsDetails": [self.single_goods_detail(sku, **kwargs) for sku in sku_code]
        }

        return express_pack

    def single_car_tray_detail(self, prod_name, sku_code: tuple, **kwargs):
        """
        组装试算卡车参数
        """
        car_tray = {
            "prodName": prod_name,
            "qty": 1,
            "weight": kwargs.get("weight", random.uniform(2, 5)),
            "length": kwargs.get("length", random.uniform(10, 30)),
            "width": kwargs.get("width", random.uniform(10, 30)),
            "height": kwargs.get("height", random.uniform(10, 30)),
            "category": kwargs.get("category", None),
            "goodsDetails": [self.single_goods_detail(sku, **kwargs) for sku in sku_code]
        }

        return car_tray

    @staticmethod
    def build_services(body, services, increase_services):

        if services and isinstance(services, tuple):
            for service in services:
                check_isinstance(service, AdditionalService, '附加服务值')
                body["services"].append(service.value)

        # 处理增值服务
        if increase_services and isinstance(increase_services, tuple):
            for service in increase_services:
                check_isinstance(service, AdditionalService, '增值服务值')
                body["increaseServices"].append(service.value)

    @staticmethod
    def build_pick_info(body, **kwargs):
        """
        组装提货信息
        Args:
            body: 参数字典

        Keyword Args:
            pick_date: 提货日期，未传时，默认为3天后 (fedex快递未来提货日期不能超过10天，卡车不能超过5天)
            min_pick: 最小提货时间
            max_pick: 最大提货时间
            min_delivery: 最小送货时间
            max_delivery: 最大送货时间
            insure_category: 投保类目
            insure_price: 投保金额
            insure_currency: 投保币种
        """
        body["pickInfo"] = {
            "pickDate": kwargs.get('pick_date', HumanDateTime().add(days=5).human_time()),
            "minPickTime": kwargs.get('min_pick', '08:00'),
            "maxPickTime": kwargs.get('max_pick', '17:00'),
            "minDeliveryTime": kwargs.get('min_delivery', '08:00'),
            "maxDeliveryTime": kwargs.get('max_delivery', '17:00'),
            "insureProdCategory": kwargs.get('insure_category'),
            "insurePrice": kwargs.get('insure_price'),
            "insureGoodsCurrency": kwargs.get('insure_currency')
        }

    @staticmethod
    def fill_package_attribute(body, **kwargs):
        """
        完善下单包裹信息
        """
        if body["transportType"] == TransportType.EXPRESS.value:
            for index, value in enumerate(body["expressPacks"]):
                value["channelId"] = kwargs.get("channel_id")
                value["sourcePackCode"] = f"来源包裹号_{HumanDateTime().timestamp()}_{index}"
                value["saleCode"] = kwargs.get("sale_code")
                value["backReason"] = kwargs.get("back_reason")
                value["faultPerson"] = kwargs.get("fault_person")

        else:
            body["carTray"]["channelId"] = kwargs.get("channel_id")
            body["carTray"]["sourcePackCode"] = f"来源包裹号_{HumanDateTime().timestamp()}"
            body["carTray"]["saleCode"] = kwargs.get("sale_code")
            body["carTray"]["backReason"] = kwargs.get("back_reason")
            body["carTray"]["faultPerson"] = kwargs.get("fault_person")

    def build_trial_body(self,
                         transport_type: TransportType,
                         address_id: int,
                         trial_country: str,
                         forward_flag: bool,
                         sku_codes: Tuple[str],
                         address_type: AddressType = None,
                         unit: UnitType = None,
                         sub_package_flag=True,
                         declare_sku_flag=False,
                         package_num=1,
                         services: Tuple[AdditionalService] = None,
                         increase_services: Tuple[AdditionalService] = None,
                         **kwargs):
        """
        试算参数组装
        Args:
            transport_type: 运输方式：快递、卡车
            address_id: 仓库地址id
            trial_country: 试算地址区域 US 美国 DE 德国 FR 法国
            address_type: 地址类型：商业地址、住宅地址、商业地址带月台、商业地址无月台
            unit: 单位  10-国标（kg/cm）；20-英制（lb/inch），默认 国标
            forward_flag: 正逆向订单标志 true:正向 false:逆向
            sku_codes: 仓库sku编码组合
            sub_package_flag: 是否需要分包：true 需要api处理分包，false 已处理分包
            declare_sku_flag: 传入申报商品标志 true: 需要传入，false: 不需要传，默认去CDS拿
            package_num: 包裹数量，默认1
            services: 附加服务，类型为tuple
            increase_services: 增值服务，类型为tuple

        Keyword Args:
            channel_id: 渠道id，类型为 tuple or int
            delivery_ware_code: 发货仓库编码，类型为 str
            source_platform: 来源平台，类型为 str
            order_category: 订单类型 10：销售订单 20：线下订单 30：补发订单
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
            "forwardFlag": forward_flag,
            "channelIds": [],
            "deliveryWareCode": kwargs.get("delivery_ware_code"),
            "sourcePlatformCode": kwargs.get("source_platform", "Python"),
            "declareSkuFlag": declare_sku_flag,
            "services": [],
            "increaseServices": []
        }

        # 正向订单，传订单类型，默认销售订单; 分包标识取传参值
        if forward_flag:
            req["orderCategory"] = kwargs.get("order_category", 10)
            req["subPackageFlag"] = sub_package_flag
        # 逆向订单，分包标识强制置为false
        else:
            req["subPackageFlag"] = False

        channels = kwargs.get('channel_id')
        if isinstance(channels, tuple):
            req["channelIds"].extend(list(channels))
        elif isinstance(channels, int):
            req["channelIds"].append(channels)

        # 处理附加服务
        self.build_services(req, services, increase_services)

        self.build_address(req, address_id, trial_country, address_type)

        # 根据快递、卡车类型，组装不同的参数体
        if req["transportType"] == TransportType.EXPRESS.value:
            if req["subPackageFlag"] and forward_flag:
                req["goodsDetails"] = [self.single_goods_detail(sku, **kwargs) for sku in sku_codes]
            else:
                req["expressPacks"] = [self.single_express_pack(f'包裹{i + 1}', sku_codes, **kwargs)
                                       for i in range(package_num)
                                       ]
        else:
            req["carTrayDetails"] = [self.single_car_tray_detail(f'托盘{i + 1}', sku_codes, **kwargs)
                                     for i in range(package_num)
                                     ]

        return req

    def build_order_body(self, transport_type: TransportType,
                         address_id: int,
                         trial_country: str,
                         forward_flag: bool,
                         sku_codes: Tuple[str],
                         address_type: AddressType = None,
                         unit: UnitType = None,
                         sub_package_flag=True,
                         declare_sku_flag=False,
                         package_num=1,
                         services: Tuple[AdditionalService] = None,
                         increase_services: Tuple[AdditionalService] = None,
                         **kwargs):
        """
        下单参数组装
        Args:
            transport_type: 运输方式：快递、卡车
            address_id: 仓库地址id
            trial_country: 试算地址区域 US 美国 DE 德国 FR 法国
            address_type: 地址类型：商业地址、住宅地址、商业地址带月台、商业地址无月台
            unit: 单位  10-国标（kg/cm）；20-英制（lb/inch），默认 国标
            forward_flag: 正逆向订单标志 true:正向 false:逆向
            sku_codes: 仓库sku编码组合
            sub_package_flag: 是否需要分包：true 需要api处理分包，false 已处理分包
            declare_sku_flag: 传入申报商品标志 true: 需要传入，false: 不需要传，默认去CDS拿
            package_num: 包裹数量，默认1
            services: 附加服务，类型为tuple
            increase_services: 增值服务，类型为tuple

        Keyword Args:
            channel_id: 渠道id，用于指定渠道下单
            pick_date: 提货日期，不传时取默认时间
            source_order_code: 来源订单号
            sale_code: 销售单号
            back_reason: 退货原因
            fault_person: 运费承担方 1.我司、2.客户、3.双方
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
            "forwardFlag": forward_flag,
            "sourceOrderCode": kwargs.get('source_order_code', f'自动测试单_{HumanDateTime().timestamp()}'),
            "assignChannelFlag": False,
            "deliveryWareCode": kwargs.get("delivery_ware_code"),
            "sourcePlatformCode": kwargs.get("source_platform", "Python"),
            "declareSkuFlag": declare_sku_flag,
            "services": [],
            "increaseServices": [],
            "remarks": "自动化测试"
        }
        # 正向订单，传订单类型，默认销售订单; 快递 分包标识取传参值
        if forward_flag and req["transportType"] == TransportType.EXPRESS.value:
            req["orderCategory"] = kwargs.get("order_category", 10)
            req["subPackageFlag"] = sub_package_flag
        # 正向订单，卡车 分包标识强制置为false
        elif forward_flag and req["transportType"] == TransportType.TRACK.value:
            req["orderCategory"] = kwargs.get("order_category", 10)
            req["subPackageFlag"] = False
        # 逆向订单，分包标识强制置为 false
        else:
            req["subPackageFlag"] = False

        # 如果有传渠道id，则认定为 指定渠道下单
        if kwargs.get('channel_id'):
            req["assignChannelFlag"] = True

        # 处理附加服务、增值服务
        self.build_services(req, services, increase_services)

        self.build_address(req, address_id, trial_country, address_type)
        self.build_pick_info(req, **kwargs)

        # 根据快递、卡车类型，组装不同的参数体
        if req["transportType"] == TransportType.EXPRESS.value:
            if req["subPackageFlag"] and forward_flag:
                req["goodsDetails"] = [self.single_goods_detail(sku, **kwargs) for sku in sku_codes]
            else:
                req["expressPacks"] = [self.single_express_pack(f'包裹{i + 1}', sku_codes, **kwargs)
                                       for i in range(package_num)
                                       ]
        else:
            req["carTray"] = {
                "trays": [self.single_car_tray_detail(f'托盘{i + 1}', sku_codes, **kwargs)
                          for i in range(package_num)
                          ]
            }

        # 已经分好包的情况下，填充一些包裹来源属性
        if not req["subPackageFlag"]:
            self.fill_package_attribute(req, **kwargs)

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

    @staticmethod
    def build_pkg_base_items(goods_info_list, reverse_sides=True):
        """
        根据跟定的货物列表计算打包成包裹的包裹属性
        :param list goods_info_list: 货物列表，格式[
            {"length": 111,
            "width":222,
            "height":333,
            "weight":88},
            {},
            ...
        ]
        :param bool reverse_sides : 是否按边长大小重排长宽高，快递传True，卡车传False
        """
        temp_result = [0, 0, 0]
        temp_weight = 0
        sku_list = []
        sorted_goods_list = sorted(goods_info_list, key=lambda s: s["weight"])
        for good in sorted_goods_list:
            length = good.get("length")
            width = good.get("width")
            height = good.get("height")
            weight = good.get("weight")
            sides = [length, width, height]
            if reverse_sides:
                sides.sort(reverse=True)
            temp_result = [max(temp_result[0], sides[0]), max(temp_result[1], sides[1]), temp_result[2] + sides[2]]
            if reverse_sides:
                temp_result.sort(reverse=True)
            temp_weight += weight

            # sku维度的属性长宽高固定需要重排
            sides.sort(reverse=True)
            sku_list.append({
                "skuWeight": weight,
                "skuSides": sides
            })
        # other_params指的是除了包裹长宽高外的其他属性，这里包含包裹总实重，sku维度的重量和边长
        other_params = [round(temp_weight, 6), sku_list]
        temp_result.extend(other_params)
        return temp_result

    def get_pkg_final_items(self, goods_list, goods_unit, channel_unit, calc_config, volume_precision,
                            reverse_length=True):
        """
        根据包裹里面sku计算得到包裹各维度数据，最终按指定的渠道信息换算配置转换为渠道换算后的包裹各维度数据，用于比较是否超出渠道限制规则
        :param list goods_list: sku列表，格式:[(长,宽,高,重),(长,宽,高,重)]
        :param int goods_unit: 货物单位,10-国际单位,20-英制单位
        :param int channel_unit: 货物属性换算的目标单位,10-国际单位,20-英制单位
        :param int calc_config: 取整方式和精度配置
        :param double volume_precision:体积重系数
        :param bool reverse_length:是否重排长宽高，用于快递
        """
        base_items = self.build_pkg_base_items(goods_list, reverse_length)
        return PackageCalcItems(*base_items, goods_unit, channel_unit, calc_config, volume_precision).package_items()

    def calc_pkg_param(self, package_data):
        """传入包裹信息，得出包裹按渠道单位、取整精度、取整方式计算出来的渠道包裹属性"""
        content = deepcopy(TMSApiConfig.CalcPackParamTest.get_attributes())
        content["data"].update(package_data)
        res = self.call_api(**content)
        return res

    def push_fms_pack(self, *package_code):
        """
        推送fms预估费用项
        :param package_code: 包裹号
        """
        content = deepcopy(TMSApiConfig.PushFMSPack.get_attributes())
        for pack in package_code:
            content["data"]["packCodes"].append(pack)

        return self.call_api(**content)

    def push_fms_express(self, package_code, old_express, new_express):
        """
        推送fms运单号变更
        :param package_code: 包裹号
        :param old_express: 旧运单号
        :param new_express: 新运单号
        """
        content = deepcopy(TMSApiConfig.PushFMSExpress.get_attributes())
        content["data"][0]["packCode"] = package_code
        content["data"][0]["oldExpressCode"] = old_express
        content["data"][0]["expressCode"] = new_express

        return self.call_api(**content)


class TMSBaseService(ServiceRobot):
    def __init__(self):
        self.dbo = TMSBaseDBO
        super().__init__('tms_base_service')

    def get_express_limit(self, country_code):
        """获取基础库字典快递限制"""
        express_limit_data = self.dbo.get_base_dict("express_limit").get("label_value")
        express_limit = json.loads(express_limit_data)
        express_limit = {key.upper(): value for key, value in express_limit.items()}
        return express_limit.get(country_code)

    def get_sub_package_limit(self, country_code):
        """获取基础库字典分包参数配置"""
        pack_limit_data = self.dbo.get_base_dict("bm_pack_limit").get("label_value")
        pack_limit_data = str_under2hump(pack_limit_data)
        pack_limit = json.loads(pack_limit_data)
        pack_limit = {key.upper(): value for key, value in pack_limit.items()}
        return pack_limit.get(country_code.upper())

    def get_package_limit(self, country_code):
        """获取基础库字典包裹限制"""
        package_limit = self.dbo.get_base_dict("package_limit")
        package_limit = {key.upper(): value for key, value in package_limit.items()}
        return package_limit.get(country_code)

    def get_sub_package(self, unit, sub_rule, good_details):
        """
        仅快递需要分包，传入货物单位、分配参数配置数据、货物列表
        :param int unit: 单位，10-国际单位，20-英制单位
        :param dict sub_rule: 分包参数配置，从数据库读取
        :param list good_details: 要分包的sku列表
        """
        content = deepcopy(TMSApiConfig.SubPackage.get_attributes())
        content["data"].update(
            {
                "unit": unit,
                "subRule": sub_rule,
                "goodsDetails": good_details

            })
        res = self.call_api(**content)
        return res.get("data")


class TMSChannelService(ServiceRobot):
    def __init__(self):
        self.order_db = LogisticOrderDBO
        self.dbo = TMSChannelDBO
        super().__init__('tms_channel_service')

    def get_ch_calc_info(self, ch_id):
        """获取渠道的试算信息，试算信息里面含渠道的单位，尺寸、重量的取整精度和方式"""
        calc_info_data = json.loads(self.dbo.get_channel_data(ch_id).get("trial_calc_info"))

        return calc_info_data

    def cancel_package(self, package_no):
        """
        取消包裹运单
        """
        content = deepcopy(TMSApiConfig.CancelPackage.get_attributes())
        content["data"]["packageNo"] = package_no

        return self.call_api(**content)

    def focus_without_time(self, *ware_codes):
        """
        执行集中下单，忽略截单时间控制
        :param ware_codes: 仓库编码
        """
        content = deepcopy(TMSApiConfig.FocusOrder.get_attributes())
        for ware in ware_codes:
            content["data"]["wareCodes"].append(ware)

        return self.call_api(**content)

    def get_tracking(self, channel_id, track_code,
                     trans_code=None, postcode=None, channel_order_code=None
                     ):
        """
        领域获取轨迹接口
        :param channel_id: 渠道id
        :param track_code: 运单号
        :param trans_code: 转运单号
        :param postcode: 收货地邮编
        :param channel_order_code: 渠道下单号
        """
        content = deepcopy(TMSApiConfig.TrackingCheck.get_attributes())
        content["data"]["channelId"] = channel_id
        content["data"]["trackCode"] = track_code
        content["data"]["transhipmentCode"] = trans_code if trans_code else ''
        if postcode:
            content["data"]["extInfo"]["postcode"] = postcode

        if channel_order_code:
            content["data"]["extInfo"]["channelOrderCode"] = channel_order_code

        if not postcode and not channel_order_code:
            content["data"].pop("extInfo", None)

        return self.call_api(**content)

    def tran_track_order(self, channel_id, trans_code):
        """
        领域获取运单号接口，传入转运单号
        :param channel_id: 渠道id
        :param trans_code: 转运单号
        """
        content = deepcopy(TMSApiConfig.BolCode.get_attributes())
        content["data"]["channelId"] = channel_id
        content["data"]["bolOrderCode"] = trans_code

        return self.call_api(**content)

    def channel_cancel_tracking(self, channel_id, package_code, express_code, trans_code=None):
        """
        领域取消运单（调用服务商接口取消，不会处理包裹状态）
        :param channel_id: 渠道id
        :param package_code: 包裹号
        :param express_code: 运单号
        :param trans_code: 转运单号
        """
        content = deepcopy(TMSApiConfig.CancelTrack.get_attributes())
        content["data"]["channelId"] = channel_id
        content["data"]["sourceOrderCode"] = package_code
        content["data"]["trackOrderCode"] = express_code
        content["data"]["transferOrderCode"] = trans_code if trans_code else ""

        return self.call_api(**content)

    def cancel_track(self, pack_code):
        """
        通过包裹号取消运单（直接调用领域）
        :param pack_code: 包裹号
        """
        express_info = self.order_db.express_order_info(
            pack_code
        )
        if not express_info:
            raise ValueError("找不到运单信息")

        return self.channel_cancel_tracking(
            channel_id=express_info['channel_id'],
            package_code=express_info['package_code'],
            express_code=express_info['express_order_code'],
            trans_code=express_info['transfer_order_code']
        )

    @staticmethod
    def calculate_all_cubic_for_wwe3(trial_body, volume_coefficient):
        """
        wwe3 试算参数计算，计算所有仓库sku的立方英尺体积、体积重、实重
        :param trial_body: 试算参数体
        :param volume_coefficient: 体积系数
        """
        cubic, weight, dim_weight = 0, 0, 0
        for car_tray in trial_body["carTrayDetails"]:
            for good in car_tray["goodsDetails"]:
                cubic += UnitChange.cm3_to_in3(
                    good["length"] * good["width"] * good["height"]
                )
                weight += UnitChange.kg_to_lb(good["weight"])
                dim_weight += UnitChange.cm3_to_in3(
                    good["length"] * good["width"] * good["height"] / volume_coefficient
                )

        cubic = Rounding.round_up(cubic / 1728, 1)
        weight = Rounding.round_up(weight, 1)
        dim_weight = Rounding.round_up(dim_weight, 1)

        return cubic, weight, dim_weight

    def tracking_by_package(self, pack_code, post_code=None):
        """
        包裹号获取服务商轨迹（直接调用领域）
        :param post_code: 收货地邮编
        :param pack_code: 包裹号
        """
        express_info = self.order_db.express_order_info(
            pack_code
        )
        if not express_info:
            raise ValueError("找不到运单信息")

        return self.get_tracking(
            channel_id=express_info['channel_id'],
            track_code=express_info['express_order_code'],
            trans_code=express_info['transfer_order_code'],
            postcode=post_code
        )


if __name__ == '__main__':
    tms_app = HomaryTMS()
    ch = TMSChannelService()
    good_unit = 20

    # 正向卡车
    # ch_id = 104
    # cn_unit = 20
    # volume_precision = 30

    # 逆向卡车
    # ch_id = 60
    # cn_unit = 10
    # volume_precision = 1111

    # 正向快递
    # ch_id = 57 #fedex-ground

    ch_id = 116
    cn_unit = 10
    volume_precision = 30

    # 逆向快递
    # ch_id = 56
    # cn_unit = 10
    # volume_precision = 30

    # 卡车货物
    # goods = [
    #     {
    #         "prodName": "HW6F57830TA01",
    #         "qty": 1,
    #         "weight": 2,
    #         "length": 15,
    #         "width": 20,
    #         "height": 30,
    #         "purchasePriceAmount": 22,
    #         "purchasePriceCurrency": "CNY",
    #         "salePriceAmount": 90,
    #         "salePriceCurrency": "USD"
    #     },
    #     {
    #         "prodName": "HW6F57830TA02",
    #         "qty": 1,
    #         "weight": 1,
    #         "length": 15,
    #         "width": 20,
    #         "height": 6,
    #         "purchasePriceAmount": 22,
    #         "purchasePriceCurrency": "CNY",
    #         "salePriceAmount": 90,
    #         "salePriceCurrency": "USD"
    #     }
    # ]

    # 正向快递货物
    # goods = [
    #     {
    #         "prodName": "HWX23A4203A02",
    #         "qty": 1,
    #         "weight": 1,
    #         "length": 15,
    #         "width": 20,
    #         "height": 30
    #     },
    #     {
    #         "prodName": "HWX23A4203A03",
    #         "qty": 1,
    #         "weight": 2,
    #         "length": 15,
    #         "width": 20,
    #         "height": 6
    #     }
    # ]

    # 逆向快递货物
    goods = [
        {
            "prodName": "HWX23A4203A02",
            "qty": 1,
            "weight": 3,
            "length": 15,
            "width": 20,
            "height": 36
        }
    ]
    calc_config = ch.get_ch_calc_info(ch_id)
    result_pkg_items = tms_app.get_pkg_final_items(goods, good_unit, cn_unit, calc_config, volume_precision, True)
    print(result_pkg_items)
