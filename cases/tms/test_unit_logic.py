from cases import homary_tms
import json
from config.third_party_api_configs.tms_api_config import TransportType, AddressType, UnitType, AdditionalService

"""
单元测试
测试自己写的方法
"""


def test_build_express_trial():
    """
    测试快递试算参数组装
    """
    transport_type = TransportType.EXPRESS
    address_id = 77
    trial_country = 'US'
    address_type = AddressType.RESIDENTIAL_ADDRESS
    channel_id = 10
    unit = UnitType.FRACTIONAL
    weight = 21.5
    sku_name = 'HHF01'
    services = AdditionalService.上门提货.value

    result = homary_tms.build_trial_body(
        transport_type, address_id, trial_country, address_type,
        unit=unit, channel_id=channel_id, weight=weight, prod_name=sku_name,
        services=services
    )
    print(json.dumps(result, ensure_ascii=False))

    assert result['transportType'] == transport_type.value, "运输阶段赋值错误"
    assert result['unit'] == unit.value, "单位类型赋值错误"
    assert result['address']['receiveAddressId'] == address_id, "地址id赋值错误"
    assert result['address']['countryCode'] == 'US', "地址国家编码错误"
    assert result['address']['addressType'] == address_type.value, "地址类型赋值错误"
    assert result['channelIds'][0] == channel_id, "渠道id赋值错误"
    assert result['expressPacks'][0]['weight'] == weight, "包裹重量赋值错误"
    assert result['expressPacks'][0]['goodsDetails'][0]['prodName'] == sku_name, "sku赋值错误"
    assert result.get('carTrayDetails') is None, "快递试算，carTrayDetails字段应该为空"


def test_build_track_trial():
    """
    测试卡车试算参数组装
    """
    transport_type = TransportType.TRACK
    address_id = 77
    trial_country = 'US'
    address_type = AddressType.BUSINESS_ADDRESS_NO_P
    channel_id = 10
    unit = UnitType.FRACTIONAL
    weight = 21.5
    sku_name = 'HHF01'
    category = '沙发'

    result = homary_tms.build_trial_body(
        transport_type, address_id, trial_country, address_type,
        unit=unit, channel_id=channel_id, weight=weight, prod_name=sku_name, category=category
    )
    print(json.dumps(result, ensure_ascii=False))
    assert result['transportType'] == transport_type.value, "运输阶段赋值错误"
    assert result['carTrayDetails'][0]['weight'] == weight, "托盘重量赋值错误"
    assert result['carTrayDetails'][0]['category'] == category, "品类赋值错误"
    assert result['carTrayDetails'][0]['goodsDetails'][0]['prodName'] == sku_name, "sku赋值错误"
    assert result['unit'] == unit.value, "单位类型赋值错误"
    assert result['address']['receiveAddressId'] == address_id, "地址id赋值错误"
    assert result['address']['countryCode'] == 'US', "地址国家编码错误"
    assert result['address']['addressType'] == address_type.value, "地址类型赋值错误"
    assert result['channelIds'][0] == channel_id, "渠道id赋值错误"


def test_build_express_order():
    """
    测试快递下单参数组装
    """
    transport_type = TransportType.EXPRESS
    address_id = 77
    trial_country = 'US'
    address_type = AddressType.RESIDENTIAL_ADDRESS
    channel_id = 10
    unit = UnitType.FRACTIONAL
    weight = 21.5
    sku_name = 'HHF01'
    pick_date = '2099-10-01 00:00:00'

    result = homary_tms.build_order_body(
        transport_type, address_id, trial_country, address_type,
        unit=unit, channel_id=channel_id, weight=weight, prod_name=sku_name,
        pick_date=pick_date
    )
    print(json.dumps(result, ensure_ascii=False))

    assert result['transportType'] == transport_type.value, "运输阶段赋值错误"
    assert result['unit'] == unit.value, "单位类型赋值错误"
    assert result['address']['receiveAddressId'] == address_id, "地址id赋值错误"
    assert result['address']['countryCode'] == 'US', "地址国家编码错误"
    assert result['address']['addressType'] == address_type.value, "地址类型赋值错误"
    assert result['expressPacks'][0]['weight'] == weight, "包裹重量赋值错误"
    assert result['expressPacks'][0]['goodsDetails'][0]['prodName'] == sku_name, "sku赋值错误"
    assert result['expressPacks'][0]['channelId'] == channel_id, "渠道id赋值错误"
    assert result['assignChannelFlag'] is True, "指定渠道断言错误"
    assert result['pickInfo']['pickDate'] == pick_date


def test_build_track_order():
    """
    测试卡车下单参数组装
    """
    transport_type = TransportType.TRACK
    address_id = 77
    trial_country = 'US'
    address_type = AddressType.BUSINESS_ADDRESS_NO_P
    channel_id = 10
    unit = UnitType.FRACTIONAL
    weight = 21.5
    sku_name = 'HHF01'
    category = '沙发'
    pick_date = '2099-10-01 00:00:00'
    insure_price = 34.5

    result = homary_tms.build_order_body(
        transport_type, address_id, trial_country, address_type,
        unit=unit, channel_id=channel_id, weight=weight, prod_name=sku_name,
        pick_date=pick_date, category=category, insure_price=insure_price
    )

    print(json.dumps(result, ensure_ascii=False))

    assert result['transportType'] == transport_type.value, "运输阶段赋值错误"
    assert result['unit'] == unit.value, "单位类型赋值错误"
    assert result['address']['receiveAddressId'] == address_id, "地址id赋值错误"
    assert result['address']['countryCode'] == 'US', "地址国家编码错误"
    assert result['address']['addressType'] == address_type.value, "地址类型赋值错误"
    assert result['carTray']['trays'][0]['weight'] == weight, "包裹重量赋值错误"
    assert result['carTray']['trays'][0]['goodsDetails'][0]['prodName'] == sku_name, "sku赋值错误"
    assert result['carTray']['channelId'] == channel_id, "渠道id赋值错误"
    assert result['assignChannelFlag'] is True, "指定渠道断言错误"
    assert result['pickInfo']['pickDate'] == pick_date
    assert result['pickInfo']['insurePrice'] == insure_price
    assert result['carTray']['trays'][0]['category'] == category, "品类赋值错误"
