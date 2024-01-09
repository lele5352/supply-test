from cases import homary_tms
from config.third_party_api_configs.tms_api_config \
    import UnitType, TransportType, AddressType, AdditionalService


def test_dx_trial():
    req = homary_tms.build_trial_body(
        TransportType.TRACK, 267, 'GB', True, sku_codes=('J04CJ000483BA01',),
        increase_services=(AdditionalService.送货到房间,)
    )
    homary_tms.do_trial(req)


def test_dx_order():
    req = homary_tms.build_order_body(
        TransportType.TRACK, 267, 'GB', True, sku_codes=('J04CJ000483BA01',),
        increase_services=(AdditionalService.送货到房间,), source_order_code='CK2401080002'
    )
    homary_tms.do_order(req)


def test_db_trial():
    req = homary_tms.build_trial_body(
        TransportType.TRACK, 120, 'FR', True, sku_codes=('J04CJ000483BA01',)
    )
    homary_tms.do_trial(req)


def test_db_order():
    req = homary_tms.build_order_body(
        TransportType.TRACK, 120, 'FR', True, sku_codes=('J04CJ000483BA01', 'J04CJ000483BA02')
    )
    homary_tms.do_order(req)

