from config.third_party_api_configs import ApiConfig, BizEnum


class FeeItemType(BizEnum):
    """费用项类型枚举"""
    LAST_FARE = (1, "尾程费用")  # 尾程费用
    RE_FARE = (2, "客退运费")  # 客退运费
    DIRECT_FARE = (3, "直发运费")  # 直发运费
    CARRIER_FARE = (4, "承运商赔款")  # 承运商赔款
    FBA_FARE = (5, "FBA运费")  # FBA运费
    SEA_FARE = (6, "海运费")  # 海运费
    SPECIAL_FARE = (99, "特殊运费")  # 特殊运费


class FeeItemCategory(BizEnum):
    """费用项分类枚举"""
    REGULAR = (1, "常规费用")  # 常规费用
    TARIFF = (2, "关税费用")  # 关税费用


class TransportType(BizEnum):
    """运输类型枚举"""
    EXPRESS = (1, "快递")
    CAR = (2, "卡车")
    SEA = (3, "海运")
    LINE = (4, "专线")
    PACKET = (5, "小包")
    INTERNAL_DIRECT = (6, "国内直发")
    INTERNAL_TRANSPORT = (7, "国内运输")
    INTERNATIONAL_TRANSPORT = (8, "国际运输")


class TransactionType(BizEnum):
    """单据类型枚举"""
    SALES = (1, "销售单")
    SEA = (2, "海运单")
    REISSUE = (3, "补发单")
    CUSTOMER_RE = (4, "客退单")


class TransportPart(BizEnum):
    """运输阶段枚举"""
    ALL = (1, "全运段")
    INTERNAL = (2, "国内运段")
    SEA = (3, "海上运段")
    CLEARANCE = (4, "国外清关")
    DELIVERY = (5, "国外派送")


class BaseApi:

    class ProviderList(ApiConfig):
        """服务商列表查询"""
        uri_path = '/api/ec-fms-api/fms/api/common/all/service/provider'
        method = "get"

    class ChannelListByProvider(ApiConfig):
        """根据服务商查询渠道列表"""
        uri_path = '/api/ec-fms-api/fms/api/common/list/channel/by/service/provider'
        method = 'get'
        data = {
            "serviceCode": ""
        }

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
        method = "POST"
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
