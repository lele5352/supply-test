import json

from cases import homary_tms
from config.third_party_api_configs.tms_api_config \
    import UnitType, TransportType, AddressType, AdditionalService


def test_trial():
    req = homary_tms.build_trial_body(
        TransportType.EXPRESS, 120, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    homary_tms.do_trial(req)


def test_order():
    req = homary_tms.build_order_body(
        TransportType.EXPRESS, 120, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    print(json.dumps(req, ensure_ascii=False))
    # homary_tms.do_order(req)


def test_focus():
    homary_tms.focus_without_time('ZY-FOR')


def test_gs_trial():
    """
    光速时代试算
    """
    req = homary_tms.build_trial_body(
        TransportType.EXPRESS, 193, 'GB', True, sku_codes=('J04CJ000483BA01',)
    )
    homary_tms.do_trial(req)


def test_gs_order():
    """
    光速时代下单
    """
    req = homary_tms.build_order_body(
        TransportType.EXPRESS, 193, 'GB', True, sku_codes=('J04CJ000483BA01',)
    )
    homary_tms.do_order(req)


def test_dx_trial():
    """
    DX 试算
    """
    req = homary_tms.build_trial_body(
        TransportType.TRACK, 267, 'GB', True, sku_codes=('J04CJ000483BA01',),
        increase_services=(AdditionalService.送货到房间,)
    )
    homary_tms.do_trial(req)


def test_dx_order():
    """
    DX 下单
    """
    req = homary_tms.build_order_body(
        TransportType.TRACK, 267, 'GB2', True, sku_codes=('J04CJ000483BA01',),
        increase_services=(AdditionalService.送货到房间,), source_order_code='CK2401090002'
    )
    homary_tms.do_order(req)


def test_db_trial():
    """
    DB 试算
    """
    req = homary_tms.build_trial_body(
        TransportType.TRACK, 120, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    homary_tms.do_trial(req)


def test_db_order():
    """
    DB 下单
    """
    req = homary_tms.build_order_body(
        TransportType.TRACK, 120, 'FR4', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02'),
        package_num=1
    )
    # print(json.dumps(req, ensure_ascii=False))
    homary_tms.do_order(req)


def test_cancel():
    """
    包裹运单取消
    """
    homary_tms.cancel_package('LP240110055869828')
