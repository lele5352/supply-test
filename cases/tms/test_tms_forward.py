import json

from cases import tms_api, tms_channel
from config.third_party_api_configs.tms_api_config \
    import UnitType, TransportType, AddressType, AdditionalService

"""
地址id:
 广州1号仓 193
 休斯顿7号仓 194
 英国7号仓 267
 加拿大大卖仓多伦多4仓 166
"""


def test_trial():
    req = tms_api.build_trial_body(
        TransportType.EXPRESS, 193, 'US', True, sku_codes=('J04CJ000483BA01', )
    )
    tms_api.do_trial(req)


def test_order():
    req = tms_api.build_order_body(
        TransportType.EXPRESS, 193, 'US', True, sku_codes=('J04CJ000483BA01', )
    )
    # print(json.dumps(req, ensure_ascii=False))
    tms_api.do_order(req)


def test_4px_trial():
    req = tms_api.build_trial_body(
        TransportType.EXPRESS, 193, 'US', True, sku_codes=('J04CJ000483BA01', )
    )
    tms_api.do_trial(req)


def test_focus():
    tms_api.focus_without_time('UKFH07')


def test_gs_trial():
    """
    光速时代试算
    """
    req = tms_api.build_trial_body(
        TransportType.EXPRESS, 193, 'DE', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


def test_gs_order():
    """
    光速时代下单
    """
    req = tms_api.build_order_body(
        TransportType.EXPRESS, 193, 'DE', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_order(req)


def test_dx_trial():
    """
    DX 试算
    """
    req = tms_api.build_trial_body(
        TransportType.TRACK, 267, 'GB', True, sku_codes=('J04CJ000483BA01',),
        increase_services=(AdditionalService.送货到房间,)
    )
    tms_api.do_trial(req)


def test_dx_order():
    """
    DX 下单
    """
    req = tms_api.build_order_body(
        TransportType.TRACK, 267, 'GB2', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02'),
        increase_services=(AdditionalService.送货到房间,), source_order_code='CK2401110003'
    )
    # print(json.dumps(req, ensure_ascii=False))
    tms_api.do_order(req)


def test_db_trial():
    """
    DB 试算
    """
    req = tms_api.build_trial_body(
        TransportType.TRACK, 120, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


def test_db_order():
    """
    DB 下单
    """
    req = tms_api.build_order_body(
        TransportType.TRACK, 120, 'FR4', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02'),
        package_num=1
    )
    # print(json.dumps(req, ensure_ascii=False))
    tms_api.do_order(req)


def test_package_cancel():
    """
    包裹运单取消
    """
    tms_api.cancel_package('LP240112055322853')


def test_express_cancel():
    """
    领域取消运单
    """
    tms_channel.cancel_by_express_code('789235327535')


def test_get_tracking():
    tms_channel.get_tracking(
        channel_id=113,
        track_code='6A32418894179'
    )
