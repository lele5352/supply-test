import json
import pytest

from cases import tms_api, tms_channel
from config.third_party_api_configs.tms_api_config \
    import TransportType, AddressType, AdditionalService
from config import order_flag

"""
地址id:
 广州1号仓 193
 广州3号仓 263
 新泽西1号仓 177
 休斯顿7号仓 194
 英国7号仓 267
 新泽西2号仓 169
 加拿大大卖仓多伦多4仓 166
"""


def test_trial():
    req = tms_api.build_trial_body(
        TransportType.TRACK, 177, 'US', forward_flag=False, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_order():
    req = tms_api.build_order_body(
        TransportType.TRACK, 177, 'US', forward_flag=False, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_order(req)


def test_fr_dpd_trial():
    req = tms_api.build_trial_body(
        TransportType.EXPRESS, 116, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_fr_dpd_order():
    req = tms_api.build_order_body(
        TransportType.EXPRESS, 116, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_order(req)


def test_wwe_trial():
    req = tms_api.build_trial_body(
        TransportType.TRACK, 177, 'US', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02')
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_wwe_order():
    req = tms_api.build_order_body(
        TransportType.TRACK, 177, 'US', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02')
    )
    tms_api.do_order(req)


def test_wwe3_trial():
    req = tms_api.build_trial_body(
        TransportType.TRACK, 169, 'US', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02'),
        increase_services=(AdditionalService.白手套,)
    )
    cubic_ft, weight, dim_weight = tms_channel.calculate_all_cubic_for_wwe3(req, 1)

    print(f"计算 cubic_ft 为 {cubic_ft}, weight 为 {weight}, dim_weight 为 {dim_weight}")
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_wwe3_order():
    req = tms_api.build_order_body(
        TransportType.TRACK, 169, 'US', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02'),
        increase_services=(AdditionalService.白手套,)
    )
    tms_api.do_order(req)


def test_yfh_trial():
    req = tms_api.build_trial_body(
        TransportType.EXPRESS, 263, 'US3', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_yfh_order():
    req = tms_api.build_order_body(
        TransportType.EXPRESS, 263, 'US3', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_order(req)


def test_parcelforce_trial():
    req = tms_api.build_trial_body(
        TransportType.EXPRESS, 267, 'GB2', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_parcelforce_order():
    """
     parcelforce 下单
     """
    req = tms_api.build_order_body(
        TransportType.EXPRESS, 267, 'GB', True, sku_codes=('J04CJ000483BA01',),
        length=104, width=52, height=8, weigth=3
    )
    # print(json.dumps(req, ensure_ascii=False))
    tms_api.do_order(req)


def test_pp_trial():
    """
    PostPony 试算
    使用新泽西2号仓
    """
    req = tms_api.build_trial_body(
        TransportType.EXPRESS, 169, 'US2', True, sku_codes=('J04CJ000483BA01',),
        length=53, width=11.5, height=11.5, weight=2
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_pp_order():
    """
     PostPony 下单
     使用新泽西2号仓
     """
    req = tms_api.build_order_body(
        TransportType.EXPRESS, 169, 'US2', True, sku_codes=('J04CJ000483BA01',),
        length=53, width=11.5, height=11.5, weight=2
    )
    # print(json.dumps(req, ensure_ascii=False))
    tms_api.do_order(req)


def test_4px_trial():
    req = tms_api.build_trial_body(
        TransportType.EXPRESS, 263, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_4px_order():
    req = tms_api.build_order_body(
        TransportType.EXPRESS, 263, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_order(req)


@pytest.mark.skipif(not order_flag, reason='不执行集中下单')
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


@pytest.mark.skipif(not order_flag, reason='不执行下单')
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


@pytest.mark.skipif(not order_flag, reason='不执行下单')
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


@pytest.mark.skipif(not order_flag, reason='不执行下单')
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


def test_turn_track():
    """
    使用转运单获取运单号
    """
    tms_channel.tran_track_order(
        channel_id=120,
        trans_code='4PX3000933371663CN'
    )


def test_package_cancel():
    """
    包裹运单取消
    """
    tms_api.cancel_package('LP240112055322853')


def test_express_cancel():
    """
    领域取消运单
    """
    tms_channel.cancel_track('LP240118055314675')


def test_get_tracking():
    tms_channel.get_tracking(
        channel_id=130,
        track_code='641U1780198'
    )


def test_push_fms_pack():
    tms_api.push_fms_pack('LP240113055569250')


def test_push_fms_express():
    tms_api.push_fms_express(
        'LP240117055359796', '3731247450', 'Y3731247450'
    )
