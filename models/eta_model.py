from peewee import *
from config import scms_db_config

database = MySQLDatabase('ec-eta', **scms_db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class CountryArea(BaseModel):
    call_code = CharField(constraints=[SQL("DEFAULT ''")])
    city_code = CharField(constraints=[SQL("DEFAULT ''")])
    code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    country_code = CharField(constraints=[SQL("DEFAULT ''")])
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    group_type = CharField(null=True)
    icon = CharField(constraints=[SQL("DEFAULT ''")])
    latitude = CharField(constraints=[SQL("DEFAULT ''")])
    level = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    longitude = CharField(constraints=[SQL("DEFAULT ''")])
    name = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    parent_id = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    sort = IntegerField(constraints=[SQL("DEFAULT 100")])
    state_code = CharField(constraints=[SQL("DEFAULT ''")])
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    zh_name = CharField(constraints=[SQL("DEFAULT ''")])
    zip_code = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'country_area'


class EcWarehouse(BaseModel):
    abroad_flag = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    city = CharField(null=True)
    country_code = CharField(null=True)
    group_type = CharField(constraints=[SQL("DEFAULT ''")])
    latitude = CharField(null=True)
    longitude = CharField(null=True)
    opening_hours = CharField(null=True)
    postal_code = CharField(null=True)
    province_code = CharField(null=True)
    self_flag = IntegerField(null=True)
    street = CharField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = IntegerField(null=True)
    warehouse_name = CharField(null=True)
    warehouse_status = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    warehouse_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    warehouse_virtual = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'ec_warehouse'


class EcWarehouseLanguage(BaseModel):
    city = CharField(null=True)
    contact_information = CharField(null=True)
    contact_person = CharField(null=True)
    country_name = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    language_code = CharField(null=True)
    language_name = CharField(null=True)
    province_name = CharField(null=True)
    warehouse_addr = CharField(null=True)
    warehouse_code = CharField()
    warehouse_id = BigIntegerField()
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'ec_warehouse_language'


class EtaEcSkuRelation(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    sku_code = CharField(null=True)
    sub_sku_code = CharField(index=True, null=True)
    sub_sku_qty = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    user_account = CharField(null=True)
    warehouse_code = CharField(null=True)

    class Meta:
        table_name = 'eta_ec_sku_relation'
        indexes = (
            (('sku_code', 'user_account'), False),
        )


class EtaOnlineSkuSiteLogistics(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_type = IntegerField(null=True)
    express_type = IntegerField(null=True)
    id = BigAutoField()
    is_suit = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    max_eta = IntegerField(null=True)
    min_eta = IntegerField(null=True)
    site_code = CharField(null=True)
    sku_code = CharField(null=True)
    sku_id = BigIntegerField(null=True)
    status = IntegerField(null=True)
    suit_sku_json = UnknownField(null=True)  # json
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)

    class Meta:
        table_name = 'eta_online_sku_site_logistics'
        indexes = (
            (('sku_code', 'site_code'), False),
        )


class EtaRule(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user = IntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    in_warehouse_max = IntegerField(null=True)
    in_warehouse_min = IntegerField(null=True)
    out_warehouse_max = IntegerField(null=True)
    out_warehouse_min = IntegerField(null=True)
    status = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = IntegerField(null=True)
    update_user_name = CharField(null=True)
    warehouse_code = CharField()
    warehouse_id = IntegerField()
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'eta_rule'


class EtaRuleLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user = IntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    eta_rule_id = IntegerField()
    operation_description = CharField(null=True)
    operation_function = CharField(null=True)
    operation_result = CharField(null=True)
    operation_time = DateTimeField(null=True)
    operator_id = IntegerField(null=True)
    operator_name = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = IntegerField(null=True)
    update_user_name = CharField(null=True)

    class Meta:
        table_name = 'eta_rule_log'


class EtaRuleLogisticsTime(BaseModel):
    country_code = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user = IntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    group_type = CharField(null=True)
    logistics_max = IntegerField(null=True)
    logistics_min = IntegerField(null=True)
    state = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = IntegerField(null=True)
    update_user_name = CharField(null=True)
    warehouse_id = IntegerField()

    class Meta:
        table_name = 'eta_rule_logistics_time'


class EtaRuleOtherTime(BaseModel):
    condition_desc = CharField()
    condition_id = IntegerField()
    condition_name = CharField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user = BigIntegerField(null=True)
    create_user_name = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    other_max = IntegerField(null=True)
    other_min = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'eta_rule_other_time'


class EtaSkuInventory(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    no_stock_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    sea_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    sell_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    sku_code = CharField(null=True)
    sku_id = BigIntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = IntegerField(null=True)

    class Meta:
        table_name = 'eta_sku_inventory'
        indexes = (
            (('sku_code', 'warehouse_id'), False),
        )


class EtaTransferOrderSku(BaseModel):
    create_time = DateTimeField(null=True)
    date_eta = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    sellable_qty = IntegerField(null=True)
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    target_warehouse_id = IntegerField(constraints=[SQL("DEFAULT 0")])
    transfer_order_code = CharField(constraints=[SQL("DEFAULT '0'")], index=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'eta_transfer_order_sku'
        indexes = (
            (('target_warehouse_id', 'sku_code'), False),
        )


class EtaWarehouseAllocation(BaseModel):
    country_code = CharField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user = IntegerField()
    del_flag = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_type = IntegerField(null=True)
    group_type = CharField(null=True)
    state = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = IntegerField(null=True)
    update_user_name = CharField(null=True)

    class Meta:
        table_name = 'eta_warehouse_allocation'
        indexes = (
            (('country_code', 'state', 'delivery_type', 'del_flag'), True),
        )


class EtaWarehouseAllocationLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user = IntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    operation_description = CharField(null=True)
    operation_function = CharField(null=True)
    operation_result = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = IntegerField(null=True)
    update_user_name = CharField(null=True)
    warehouse_allocation_id = IntegerField()

    class Meta:
        table_name = 'eta_warehouse_allocation_log'


class EtaWarehouseAllocationWarehouse(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user = IntegerField(null=True)
    del_flag = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    group_type = CharField(null=True)
    level = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = IntegerField(null=True)
    update_user_name = CharField(null=True)
    warehouse_allocation_id = IntegerField()
    warehouse_code = CharField()
    warehouse_id = IntegerField()
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'eta_warehouse_allocation_warehouse'
        indexes = (
            (('warehouse_allocation_id', 'warehouse_id', 'del_flag'), True),
        )


class GoodsSkuInventory(BaseModel):
    available_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    bom_version = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_warehouse = CharField(index=True, null=True)
    delivery_warehouse_locate_region = IntegerField(null=True)
    demand_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    eta_time = DecimalField(constraints=[SQL("DEFAULT 0.0")], null=True)
    goods_sku_code = CharField(index=True, null=True)
    inventory_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    inventory_type = IntegerField()
    max_time = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    min_time = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    oms_order_no = CharField(null=True)
    site_deliver_type = UnknownField(null=True)  # json
    source_no = CharField(null=True)
    start_warehouse = CharField(null=True)
    start_warehouse_locate_region = IntegerField(null=True)
    stock_order_eta = DateTimeField(null=True)
    time_unit = CharField(null=True)
    virtual_delivery_warehouse = CharField(null=True)
    virtual_start_warehouse = CharField(null=True)

    class Meta:
        table_name = 'goods_sku_inventory'


class OmsSkuBlock(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_code = CharField(index=True)
    post_code_group_no = IntegerField(index=True)
    total_block = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'oms_sku_block'


class PostCodeGroupAverageEta(BaseModel):
    average_eta_max_customer = IntegerField()
    average_eta_max_warehouse = IntegerField()
    average_eta_min_customer = IntegerField()
    average_eta_min_warehouse = IntegerField()
    country = CharField(index=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    post_code = CharField(index=True)
    post_code_group_no = IntegerField(index=True)
    sea_average_eta_max = IntegerField()
    sea_average_eta_min = IntegerField()
    time_unit = CharField()
    warehouse = CharField()
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'post_code_group_average_eta'


class PostCodeGroupAverageEtaV2(BaseModel):
    average_eta_max_customer = IntegerField()
    average_eta_max_warehouse = IntegerField()
    average_eta_min_customer = IntegerField()
    average_eta_min_warehouse = IntegerField()
    country = CharField(index=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    post_code = CharField(index=True)
    post_code_group_no = IntegerField(index=True)
    sea_average_eta_max = IntegerField()
    sea_average_eta_min = IntegerField()
    time_unit = CharField()
    warehouse = CharField()
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'post_code_group_average_eta_v2'


class PostCodeGroupAverageEtaV3(BaseModel):
    arrived_warehouse_max = IntegerField()
    arrived_warehouse_min = IntegerField()
    country = CharField(index=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    in_warehouse_max = IntegerField()
    in_warehouse_min = IntegerField()
    out_warehouse_max = IntegerField()
    out_warehouse_min = IntegerField()
    post_code = CharField(index=True)
    post_code_group_no = IntegerField(index=True)
    sea_eta_max = IntegerField()
    sea_eta_min = IntegerField()
    time_unit = CharField()
    warehouse = CharField()
    warehouse_id = BigIntegerField()
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'post_code_group_average_eta_v3'


class PostCodeGroupDeliveryType(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_type = IntegerField()
    post_code_group_id = IntegerField(index=True)

    class Meta:
        table_name = 'post_code_group_delivery_type'


class PostCodeGroupDeliveryTypeV2(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_type = IntegerField()
    post_code_group_id = IntegerField(index=True)

    class Meta:
        table_name = 'post_code_group_delivery_type_v2'


class PostCodeGroupDeliveryTypeV3(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_type = IntegerField()
    logistics_max = IntegerField()
    logistics_min = IntegerField()
    post_code_group_id = IntegerField(index=True)
    warehouse_level = IntegerField()

    class Meta:
        table_name = 'post_code_group_delivery_type_v3'


class SkuAvailableStock(BaseModel):
    available_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)

    class Meta:
        table_name = 'sku_available_stock'


class SkuAvailableStockV2(BaseModel):
    available_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)

    class Meta:
        table_name = 'sku_available_stock_v2'


class SkuAvailableStockV3(BaseModel):
    available_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)

    class Meta:
        table_name = 'sku_available_stock_v3'


class SkuAvailableStockV4(BaseModel):
    available_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)

    class Meta:
        table_name = 'sku_available_stock_v4'


class SkuDefaultPurchaseDelivery(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_code = CharField(index=True)
    purchase_delivery = IntegerField()
    supplier_id = BigIntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)

    class Meta:
        table_name = 'sku_default_purchase_delivery'


class WareSkuInventory(BaseModel):
    bom_qty = IntegerField(null=True)
    bom_version = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_code = CharField(index=True, null=True)
    goods_sku_inventory_id = IntegerField(index=True, null=True)
    goods_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ware_sku_code = CharField(index=True, null=True)
    ware_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'ware_sku_inventory'
