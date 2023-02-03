from config.third_party_api_configs import ApiConfig
from enum import Enum


class FmsEnum:

    class FeeItemType(Enum):
        """费用项类型枚举"""
        LAST_FARE = {"name": "尾程费用", "value": 1}  # 尾程费用
        RE_FARE = {"name": "客退运费", "value": 2}  # 客退运费
        DIRECT_FARE = {"name": "直发运费", "value": 3}  # 直发运费
        CARRIER_FARE = {"name": "承运商赔款", "value": 4}  # 承运商赔款
        FBA_FARE = {"name": "FBA运费", "value": 5}  # FBA运费
        SEA_FARE = {"name": "海运费", "value": 6}  # 海运费
        SPECIAL_FARE = {"name": "特殊运费", "value": 99}  # 特殊运费

    class FeeItemCategory(Enum):
        """费用项分类枚举"""
        REGULAR = {"name": "常规费用", "value": 1}  # 常规费用
        TARIFF = {"name": "关税费用", "value": 2}  # 关税费用

    class TransportType(Enum):
        """运输类型枚举"""
        EXPRESS = {"name": "快递", "value": 1}
        CAR = {"name": "卡车", "value": 2}
        SEA = {"name": "海运", "value": 3}
        LINE = {"name": "专线", "value": 4}
        PACKET = {"name": "小包", "value": 5}
        INTERNAL_DIRECT = {"name": "国内直发", "value": 6}
        INTERNAL_TRANSPORT = {"name": "国内运输", "value": 7}
        INTERNATIONAL_TRANSPORT = {"name": "国际运输", "value": 8}

    class TransactionType(Enum):
        """单据类型枚举"""
        SALES = {"name": "销售单", "value": 1}
        SEA = {"name": "海运单", "value": 2}
        REISSUE = {"name": "补发单", "value": 3}
        CUSTOMER_RE = {"name": "客退单", "value": 4}

    class TransportPart(Enum):
        """运输阶段枚举"""
        ALL = {"name": "全运段", "value": 1}
        INTERNAL = {"name": "国内运段", "value": 2}
        SEA = {"name": "海上运段", "value": 3}
        CLEARANCE = {"name": "国外清关", "value": 4}
        DELIVERY = {"name": "国外派送", "value": 5}


class BaseApi:

    class ProviderList(ApiConfig):
        """服务商列表查询"""
        uri_path = '/api/ec-fms-api/fms/api/common/all/service/provider'
        method = "get"

    class ChannelList(ApiConfig):
        """渠道列表查询"""
        uri_path = '/api/ec-fms-api/fms/api/common/all/channel'
        method = 'get'

    class GetOmsOrder(ApiConfig):
        """查oms订单详情"""
        uri_path = '/api/ec-fms-api/fms/api/common/all/channel'
        method = 'get'
        data = {
            "outStockNo": ""
        }


class FeeRateApi:

    class PullFeeRate(ApiConfig):
        """汇率拉取"""
        uri_path = '/api/ec-fms-api/fms/fee-rate/pull'
        method = 'get'

    class FeeRatePage(ApiConfig):
        """汇率列表查询"""
        uri_path = '/api/ec-fms-api/fms/api/currency-rate/page'
        method = 'post'
        data = {"currencyTime": "", "baseCurrency": "", "toCurrency": "", "current": 1, "size": 10, "total": 0}


class FeeItemApi:

    class FeeItemPage(ApiConfig):
        """费用项列表分页查询"""
        uri_path = '/api/ec-fms-api/fms/fee-item/page'
        method = "post"
        data = {"feeItemName": "", "feeItemType": [], "feeItemCategory": "", "pageSize": 10, "pageNumber": 1,
                "total": 99}

    class FeeItemList(ApiConfig):
        """
        费用项列表查询（不分页）
        """
        uri_path = '/api/ec-fms-api/fms/fee-item/list'
        method = 'post'
        data = {}

    class FeeItemAdd(ApiConfig):
        """费用项新增"""
        uri_path = '/api/ec-fms-api/fms/fee-item/add'
        method = 'post'
        data = {"feeItemName": "", "feeItemType": None, "feeItemCategory": None, "remark": "", "id": None}


class ExpectFeeItemApi:

    class ExpectFeeItemPage(ApiConfig):
        """预估费用项列表查询，分页"""
        uri_path = '/api/ec-fms-api/fms/expect-fee-item/page'
        method = 'post'
        data = {"checkBillTimeEnd": "", "confirmTimeEnd": "", "transportPart": [], "feeItemName": [],
                "confirmTimeStart": "", "transactionType": [], "outStockNo": [], "deliveryNo": [], "createTimeEnd": "",
                "channel": [], "packageNo": [], "servicer": [], "checkBillTimeStart": "", "shippingTimeStart": "",
                "expectFeeItemStatus": [], "createTimeStart": "", "shippingTimeEnd": "", "shippingTime": [],
                "createTime": [], "checkBillTime": [], "confirmTime": [], "transportTypes": [], "expectType": None,
                "shippingPlace": "", "destination": "", "shippingWarehouses": [], "pageSize": 10, "pageNumber": 1,
                "total": 0}

    class NotSeaExpectFeeItemSave(ApiConfig):
        """非海运，预估费用项新增"""
        uri_path = '/api/ec-fms-api/fms/expect-fee-item/save/notSeaExpectFeeItem'
        method = 'post'
        data = {"transactionType": None, "shippingPlace": "", "shippingWarehouse": "", "destination": "",
                "servicer": "", "channel": "", "transportType": None, "shippingTime": "",
                "goodsAmount": "", "salesAmount": "", "salesAmountCurrency": "",
                "declareCustomsAmount": "", "declareCustomsAmountCurrency": "",
                "expectFeeItemPackageDetails": [],
                "expectFeeItemDetails": [],
                "deliveryNo": "", "outStockNo": "", "chargedWeight": "",
                "chargedWeightUnit": "", "provinceCode": "", "postCode": ""}
