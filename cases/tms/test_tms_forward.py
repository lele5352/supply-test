import json
import pytest

from cases import tms_api, tms_channel
from config.third_party_api_configs.tms_api_config \
    import TransportType, AddressType, AdditionalService


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

# 导入是否下单标识，控制下单用例执行
try:
    from config import order_flag
except ImportError:
    order_flag = False


def test_trial():
    """
    试算调试
    """
    req = tms_api.build_trial_body(
        TransportType.TRACK, 177, 'US', forward_flag=False, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_order():
    """
    下单调试
    """
    req = tms_api.build_order_body(
        TransportType.TRACK, 177, 'US', forward_flag=False, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_order(req)


def test_fr_dpd_trial():
    """
    法国DPD 试算
    """
    req = tms_api.build_trial_body(
        TransportType.EXPRESS, 116, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_fr_dpd_order():
    """
    法国DPD 下单
    """
    req = tms_api.build_order_body(
        TransportType.EXPRESS, 116, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_order(req)


def test_uk_dpd_trial():
    """
    英国DPD 试算
    """
    req = tms_api.build_trial_body(
        transport_type=TransportType.EXPRESS,
        address_id=116,
        trial_country='GB',
        forward_flag=True,
        sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_uk_dpd_order():
    """
    英国DPD 下单
    """
    req = tms_api.build_order_body(
        TransportType.EXPRESS, 116, 'GB', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_order(req)


def test_wwe_trial():
    """
    WWE 试算
    """
    req = tms_api.build_trial_body(
        TransportType.TRACK, 177, 'US', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02')
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_wwe_order():
    """
    WWE 下单
    """
    req = tms_api.build_order_body(
        TransportType.TRACK, 177, 'US', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02')
    )
    tms_api.do_order(req)


def test_wwe3_trial():
    """
    WWE3 试算
    """
    req = tms_api.build_trial_body(
        TransportType.TRACK, 169, 'US', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02'),
        increase_services=(AdditionalService.白手套,)
    )
    cubic_ft, weight, dim_weight = tms_channel.calculate_all_cubic_for_wwe3(req, 1)

    print(f"计算 cubic_ft 为 {cubic_ft}, weight 为 {weight}, dim_weight 为 {dim_weight}")
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_wwe3_order():
    """
    WWE3 下单
    """
    req = tms_api.build_order_body(
        TransportType.TRACK, 169, 'US', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02'),
        increase_services=(AdditionalService.白手套,)
    )
    tms_api.do_order(req)


def test_yfh_trial():
    """
    原飞航 试算
    """
    req = tms_api.build_trial_body(
        TransportType.EXPRESS, 263, 'US3', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_yfh_order():
    """
    原飞航 下单
    """
    req = tms_api.build_order_body(
        TransportType.EXPRESS, 263, 'US3', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_order(req)


def test_parcelforce_trial():
    """
    parcelforce 试算
    """
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
    """
    4PX 试算
    """
    req = tms_api.build_trial_body(
        TransportType.EXPRESS, 263, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_trial(req)


@pytest.mark.skipif(not order_flag, reason='不执行下单')
def test_4px_order():
    """
    4PX 下单
    """
    req = tms_api.build_order_body(
        TransportType.EXPRESS, 263, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    tms_api.do_order(req)


@pytest.mark.skipif(not order_flag, reason='不执行集中下单')
def test_focus():
    """
    调用集中下单
    """
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
    tms_channel.cancel_track('LP240119055816531')


def test_get_tracking():
    """
    调用channel领域，获取服务商轨迹
    """
    tms_channel.get_tracking(
        channel_id=130,
        track_code='641U1780198'
    )


def test_push_fms_pack():
    """
    推送fms预估费用项
    """
    tms_api.push_fms_pack('LP240113055569250')


def test_push_fms_express():
    """
    推送fms运单号变更
    """
    tms_api.push_fms_express(
        'LP240117055359796', '3731247450', 'Y3731247450'
    )
