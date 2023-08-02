from peewee import *
from config import scms_db_config

database = MySQLDatabase('supply_oms', **scms_db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class EcOrderMap(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    ec_order_no = CharField(null=True)
    ec_ref_no = CharField(null=True)
    id = BigAutoField()
    sales_order_no = CharField(null=True)
    warehouse_order_no = CharField(null=True)

    class Meta:
        table_name = 'ec_order_map'


class EcSkuRelation(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = CharField(null=True)
    create_user_id = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    sku_code = CharField(null=True)
    sub_sku_code = CharField(index=True, null=True)
    sub_sku_qty = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = CharField(null=True)
    update_user_id = BigIntegerField(null=True)
    versions = CharField(null=True)

    class Meta:
        table_name = 'ec_sku_relation'
        indexes = (
            (('sku_code', 'versions'), False),
        )


class EtaOrderItem(BaseModel):
    arrival_user_date_max = DateField(null=True)
    arrival_user_date_min = DateField(null=True)
    arrival_warehouse_date_max = DateField(null=True)
    arrival_warehouse_date_min = DateField(null=True)
    bad_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    country = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    eta_order_item_status = IntegerField()
    id = BigAutoField()
    last_pick_up_fcl_date = DateField(null=True)
    oms_order_no = CharField(index=True)
    pick_up_fcl_date = DateField(null=True)
    push_status = IntegerField()
    sale_order_no = CharField(index=True)
    sku_code = CharField(index=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()

    class Meta:
        table_name = 'eta_order_item'


class EtaOrderItemPushLog(BaseModel):
    arrival_user_date_max = DateField(null=True)
    arrival_user_date_min = DateField(null=True)
    arrival_warehouse_date_max = DateField(null=True)
    arrival_warehouse_date_min = DateField(null=True)
    bad_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    country = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    eta_order_item_id = BigIntegerField(index=True)
    eta_order_item_status = IntegerField()
    id = BigAutoField()
    last_pick_up_fcl_date = DateField(null=True)
    oms_order_no = CharField()
    pick_up_fcl_date = DateField(null=True)
    sale_order_no = CharField()
    sku_code = CharField()

    class Meta:
        table_name = 'eta_order_item_push_log'


class EtaShippingRule(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    export_actual = DecimalField(constraints=[SQL("DEFAULT 0.0")])
    export_max = IntegerField()
    export_min = IntegerField()
    id = BigAutoField()
    importing_actual = DecimalField(constraints=[SQL("DEFAULT 0.0")])
    importing_max = IntegerField()
    importing_min = IntegerField()
    port_pickup_actual = DecimalField(constraints=[SQL("DEFAULT 0.0")])
    port_pickup_max = IntegerField()
    port_pickup_min = IntegerField()
    to_warehouse_actual = DecimalField(constraints=[SQL("DEFAULT 0.0")])
    to_warehouse_max = IntegerField()
    to_warehouse_min = IntegerField()
    transporting_actual = DecimalField(constraints=[SQL("DEFAULT 0.0")])
    transporting_max = IntegerField()
    transporting_min = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    waiting_import_actual = DecimalField(constraints=[SQL("DEFAULT 0.0")])
    waiting_import_max = IntegerField()
    waiting_import_min = IntegerField()
    warehouse_code = CharField()
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'eta_shipping_rule'
        indexes = (
            (('warehouse_code', 'create_time', 'del_flag'), True),
        )


class EtaWarehouseRule(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    in_warehouse_actual = DecimalField(constraints=[SQL("DEFAULT 0.0")])
    in_warehouse_max = IntegerField()
    in_warehouse_min = IntegerField()
    out_warehouse_actual = DecimalField(constraints=[SQL("DEFAULT 0.0")])
    out_warehouse_max = IntegerField()
    out_warehouse_min = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    warehouse_code = CharField()
    warehouse_id = BigIntegerField()
    warehouse_name = CharField(null=True)
    warehouse_rule_status = IntegerField()
    warehouse_type = IntegerField()

    class Meta:
        table_name = 'eta_warehouse_rule'
        indexes = (
            (('warehouse_code', 'create_time', 'del_flag'), True),
        )


class EtaWarehouseRuleLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    operation_description = CharField(null=True)
    operation_type = IntegerField()
    warehouse_rule_id = BigIntegerField()

    class Meta:
        table_name = 'eta_warehouse_rule_log'


class EtaWarehouseRuleLogistics(BaseModel):
    country_code = CharField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    logistics_actual = DecimalField(constraints=[SQL("DEFAULT 0.0")])
    logistics_max = IntegerField()
    logistics_min = IntegerField()
    post_code = CharField()
    post_code_type = IntegerField()
    transport_type = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    warehouse_code = CharField()
    warehouse_rule_id = BigIntegerField()

    class Meta:
        table_name = 'eta_warehouse_rule_logistics'


class GoodSkuReport(BaseModel):
    central_block = IntegerField()
    central_shortage = IntegerField()
    central_stock = IntegerField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    delivery_on_way_stock = IntegerField()
    delivery_stock = IntegerField()
    goods_sku_code = CharField(index=True)
    goods_stock = IntegerField()
    handle_date = CharField()
    id = BigAutoField()
    plan_on_way_amount = IntegerField()
    prepare_all_stock = IntegerField()
    target_warehouse_name = CharField()
    transfer_purchase_amount = IntegerField()
    transit_purchase_stock = IntegerField()
    transit_stock = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField()

    class Meta:
        table_name = 'good_sku_report'
        indexes = (
            (('handle_date', 'version'), True),
        )


class OmsBrandWarehouseConfig(BaseModel):
    brand = CharField()
    brand_id = BigIntegerField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = CharField(constraints=[SQL("DEFAULT ''")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    update_user_id = BigIntegerField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'oms_brand_warehouse_config'


class OmsCommand(BaseModel):
    after_sales_reason = CharField(null=True)
    command_code = CharField(index=True)
    content = UnknownField()  # json
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = CharField(null=True)
    create_user_id = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    mall_msg = UnknownField(null=True)  # json
    push_mall_status = IntegerField(constraints=[SQL("DEFAULT 1")])
    sales_order_no = CharField(index=True)
    source = IntegerField()
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = CharField(null=True)
    update_user_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'oms_command'


class OmsCommandDetail(BaseModel):
    command_id = BigIntegerField(index=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    demand_qty = IntegerField()
    id = BigAutoField()
    intercept_command_id = IntegerField(null=True)
    intercept_reason = IntegerField(constraints=[SQL("DEFAULT -1")], null=True)
    intercept_type = IntegerField()
    order_id = BigIntegerField(index=True)
    order_no = CharField(index=True)
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    status = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'oms_command_detail'


class OmsDemand(BaseModel):
    bom_version = CharField(null=True)
    cancel_time = DateTimeField(null=True)
    complete_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = CharField(null=True)
    create_user_id = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_target_warehouse_code = CharField(null=True)
    delivery_target_warehouse_id = BigIntegerField(null=True)
    delivery_target_warehouse_name = CharField(null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(null=True)
    demand_status = IntegerField()
    demand_type = IntegerField()
    extern_demand_no = CharField(null=True)
    id = BigAutoField()
    item_picture = CharField(null=True)
    item_sku_code = CharField()
    item_sku_type = IntegerField(null=True)
    link_no = CharField()
    purchase_status = IntegerField(null=True)
    quantity = IntegerField()
    receive_target_warehouse_code = CharField(null=True)
    receive_target_warehouse_id = BigIntegerField(null=True)
    receive_target_warehouse_name = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    remark = CharField(null=True)
    transfer_status = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = CharField(null=True)
    update_user_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'oms_demand'


class OmsDividingRules(BaseModel):
    country_code = CharField(null=True)
    country_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_type = IntegerField()
    express_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    status = IntegerField()
    type = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = CharField(null=True)

    class Meta:
        table_name = 'oms_dividing_rules'


class OmsDividingRulesPostcode(BaseModel):
    country_code = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    dividing_rules_id = BigIntegerField()
    id = BigAutoField()
    post_code = CharField()
    type = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = IntegerField()

    class Meta:
        table_name = 'oms_dividing_rules_postcode'


class OmsDividingRulesWarehouse(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    dividing_rules_id = BigIntegerField()
    id = BigAutoField()
    level = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = IntegerField()
    warehouse_code = CharField()
    warehouse_name = CharField()

    class Meta:
        table_name = 'oms_dividing_rules_warehouse'


class OmsExportTask(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = CharField(null=True)
    create_user_id = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    export_type = IntegerField(null=True)
    file_name = CharField()
    id = BigAutoField()
    state = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = CharField(null=True)
    update_user_id = BigIntegerField(null=True)
    url = CharField(null=True)

    class Meta:
        table_name = 'oms_export_task'


class OmsFileImport(BaseModel):
    create_time = DateTimeField(null=True)
    create_user = IntegerField(null=True)
    create_user_name = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    error_qty = IntegerField(null=True)
    file_name = CharField(null=True)
    file_url = CharField(null=True)
    status = IntegerField(null=True)
    type = IntegerField(null=True)

    class Meta:
        table_name = 'oms_file_import'


class OmsFileImportDetail(BaseModel):
    create_time = DateTimeField(null=True)
    create_user = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    file_import_id = IntegerField(null=True)
    message = CharField(null=True)
    row_num = IntegerField(null=True)
    state = IntegerField(null=True)
    valid_status = IntegerField(null=True)

    class Meta:
        table_name = 'oms_file_import_detail'


class OmsFollowChange(BaseModel):
    arriving_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    bom_version = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    delivery_warehouse_id = BigIntegerField()
    delivery_warehouse_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    id = BigAutoField()
    in_stock_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    item_sku_code = CharField(index=True)
    lack_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    latest = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    order_no = CharField(index=True)
    plan_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_order_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    sales_order_no = CharField(index=True)
    subscribe_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    transit_pre_on_way_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    transit_prepare_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    transit_purchase_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    transit_subscribe_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'oms_follow_change'


class OmsFollowPrepareBlock(BaseModel):
    block_number = IntegerField()
    bom_version = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_code = CharField()
    handle_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    item_category_id = BigIntegerField()
    item_category_name = CharField()
    item_picture = CharField(constraints=[SQL("DEFAULT ''")])
    item_sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    item_sku_type = IntegerField()
    order_id = BigIntegerField()
    order_no = CharField()
    prepare_warehouse_code = CharField()
    prepare_warehouse_id = BigIntegerField()
    prepare_warehouse_name = CharField()
    sales_order_no = CharField()
    target_warehouse_code = CharField()
    target_warehouse_id = BigIntegerField()
    target_warehouse_name = CharField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)
    virtual_prepare_warehouse_code = CharField()
    virtual_prepare_warehouse_id = BigIntegerField()
    virtual_prepare_warehouse_name = CharField()
    virtual_target_warehouse_code = CharField()
    virtual_target_warehouse_id = BigIntegerField()
    virtual_target_warehouse_name = CharField()

    class Meta:
        table_name = 'oms_follow_prepare_block'


class OmsFollowStockOrder(BaseModel):
    common_warehouse_code = CharField(null=True)
    common_warehouse_id = BigIntegerField(null=True)
    common_warehouse_name = CharField(null=True)
    container_no = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    eta = DateTimeField(null=True)
    execute_overdue = IntegerField(null=True)
    follow_preempt_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_code = CharField(null=True)
    id = BigAutoField()
    item_sku_code = CharField()
    max_eta = DateTimeField(null=True)
    min_eta = DateTimeField(null=True)
    not_contain_cur_eta = DateTimeField(null=True)
    not_contain_cur_max_eta = DateTimeField(null=True)
    not_contain_cur_min_eta = DateTimeField(null=True)
    order_follow_id = BigIntegerField(index=True, null=True)
    order_no = CharField(null=True)
    order_type = IntegerField()
    overdue_reason = CharField(null=True)
    plan_performance_eta = UnknownField(null=True)  # json
    preempt_haft_flag = IntegerField(constraints=[SQL("DEFAULT -1")], null=True)
    preempt_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    remain_duration = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    target_warehouse_code = CharField()
    target_warehouse_id = BigIntegerField()
    target_warehouse_name = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)
    virtual_warehouse_code = CharField(null=True)
    virtual_warehouse_id = BigIntegerField(null=True)
    virtual_warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'oms_follow_stock_order'


class OmsFollowStockOrderBak0113(BaseModel):
    container_no = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    eta = DateTimeField(null=True)
    id = BigAutoField()
    item_sku_code = CharField()
    order_follow_id = BigIntegerField(index=True, null=True)
    order_no = CharField()
    order_type = IntegerField()
    preempt_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_warehouse_code = CharField()
    target_warehouse_id = BigIntegerField()
    target_warehouse_name = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)

    class Meta:
        table_name = 'oms_follow_stock_order_bak0113'


class OmsFollowStockOrderBak0320(BaseModel):
    container_no = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    eta = DateTimeField(null=True)
    id = BigAutoField()
    item_sku_code = CharField()
    order_follow_id = BigIntegerField(index=True, null=True)
    order_no = CharField()
    order_type = IntegerField()
    preempt_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_warehouse_code = CharField()
    target_warehouse_id = BigIntegerField()
    target_warehouse_name = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)

    class Meta:
        table_name = 'oms_follow_stock_order_bak0320'


class OmsGoodSkuReport(BaseModel):
    central_block = IntegerField()
    central_shortage = IntegerField()
    central_stock = IntegerField()
    central_virtual_block = IntegerField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    delivery_on_way_stock = IntegerField()
    delivery_stock = IntegerField()
    goods_sku_code = CharField(index=True)
    goods_stock = IntegerField()
    handle_date = CharField()
    id = BigAutoField()
    prepare_all_stock = IntegerField()
    purchase_order_qty = IntegerField()
    short_demand_qty = IntegerField()
    subscribe_plan_qty = IntegerField()
    target_warehouse_name = CharField()
    transfer_plan_qty = IntegerField()
    transit_purchase_on_way = IntegerField()
    transit_stock = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField()

    class Meta:
        table_name = 'oms_good_sku_report'
        indexes = (
            (('handle_date', 'version'), False),
        )


class OmsGoodSkuReportBak(BaseModel):
    central_block = IntegerField()
    central_shortage = IntegerField()
    central_stock = IntegerField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    delivery_on_way_stock = IntegerField()
    delivery_stock = IntegerField()
    goods_sku_code = CharField(index=True)
    goods_stock = IntegerField()
    handle_date = CharField()
    id = BigAutoField()
    plan_on_way_amount = IntegerField()
    prepare_all_stock = IntegerField()
    target_warehouse_name = CharField()
    transfer_purchase_amount = IntegerField()
    transit_purchase_stock = IntegerField()
    transit_stock = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField()

    class Meta:
        table_name = 'oms_good_sku_report_bak'
        indexes = (
            (('handle_date', 'version'), False),
        )


class OmsInterfaceLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    id = BigAutoField()
    keyword_type = CharField(null=True)
    keyword_value = CharField(index=True, null=True)
    operate_describe = CharField(null=True)
    request_content = TextField()
    result_content = TextField(null=True)
    trace_id = CharField(null=True)
    url = CharField(null=True)

    class Meta:
        table_name = 'oms_interface_log'


class OmsLackGoodsDemand(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    delivery_warehouse_name = CharField(constraints=[SQL("DEFAULT ''")])
    demand_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    eta = CharField(constraints=[SQL("DEFAULT ''")])
    eta_warehouse = CharField(constraints=[SQL("DEFAULT ''")])
    id = BigAutoField()
    int_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    int_warehouse_name = CharField(null=True)
    issued_time = DateTimeField(null=True)
    item_category_id = BigIntegerField(null=True)
    item_category_name = CharField(null=True)
    item_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    order_no = CharField(constraints=[SQL("DEFAULT ''")])
    order_status = IntegerField(constraints=[SQL("DEFAULT 0")])
    out_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    out_warehouse_name = CharField(null=True)
    pay_time = DateTimeField(null=True)
    purchase_no = CharField(constraints=[SQL("DEFAULT ''")])
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    receive = CharField(constraints=[SQL("DEFAULT ''")])
    receive_status = IntegerField(constraints=[SQL("DEFAULT 0")])
    sales_order_no = CharField(constraints=[SQL("DEFAULT ''")])
    transfer_no = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'oms_lack_goods_demand'


class OmsLinkOrderFollow(BaseModel):
    city = CharField(null=True)
    country = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_time = DateTimeField(null=True)
    eta_time_out = IntegerField(null=True)
    id = BigAutoField()
    item_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    item_status = IntegerField(null=True)
    order_eta = DateTimeField(null=True)
    pay_time = DateTimeField(null=True)
    platform_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    platform_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    postal_code = CharField(null=True)
    predict_over_eta = IntegerField(null=True)
    product_eta = DateTimeField(null=True)
    province = CharField(null=True)
    sales_order_no = CharField()
    site_code = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)

    class Meta:
        table_name = 'oms_link_order_follow'


class OmsLogisticsCleanInfo(BaseModel):
    channel_code = CharField(null=True)
    clean_delivered_at = DateTimeField(null=True)
    country_code = CharField()
    country_name = CharField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_user_name = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivered_at = DateTimeField(null=True)
    delivery_no = CharField()
    delivery_time = DateTimeField(null=True)
    exception_status = IntegerField(null=True)
    first_appointment_at = DateTimeField(null=True)
    first_contact_at = DateTimeField(null=True)
    id = BigAutoField()
    issue_time = DateTimeField(null=True)
    logistics_no = CharField(unique=True)
    postal_code = CharField()
    re_check_time = DateTimeField(null=True)
    site_code = CharField()
    transport_type = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = BigIntegerField(null=True)
    update_user_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    virtual_warehouse_code = CharField()
    virtual_warehouse_name = CharField()
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'oms_logistics_clean_info'


class OmsLogisticsInfo(BaseModel):
    channel_code = CharField(null=True)
    check_point = UnknownField(null=True)  # json
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_user_name = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivered_at = DateTimeField(null=True)
    delivery_no = CharField()
    delivery_time = DateTimeField(null=True)
    exception_id = IntegerField(null=True)
    exception_name = CharField(null=True)
    exception_status = IntegerField(null=True)
    first_appointment_at = DateTimeField(null=True)
    first_contact_at = DateTimeField(null=True)
    id = BigAutoField()
    is_overdue = IntegerField(null=True)
    logistics_no = CharField(unique=True)
    overdue_reason = CharField(null=True)
    package_no = CharField()
    slug = CharField(null=True)
    status = CharField(null=True)
    status_cn = CharField(null=True)
    tracking_number = CharField(null=True)
    tracking_service = CharField(null=True)
    transport_type = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = BigIntegerField(null=True)
    update_user_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)

    class Meta:
        table_name = 'oms_logistics_info'


class OmsOrder(BaseModel):
    address = CharField(null=True)
    address1 = CharField(null=True)
    address2 = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    address3 = CharField(null=True)
    buyer_id = CharField(null=True)
    buyer_name = CharField(null=True)
    cancel_time = DateTimeField(null=True)
    city = CharField(null=True)
    company = CharField(null=True)
    country = CharField(index=True, null=True)
    country_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = CharField(constraints=[SQL("DEFAULT ''")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    credit_card_type = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_time = DateTimeField(null=True)
    delivery_time_end = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    delivery_time_start = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    delivery_type = IntegerField(null=True)
    delivery_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(constraints=[SQL("DEFAULT ''")])
    email = CharField(null=True)
    ext_info = UnknownField(null=True)  # json
    first_name = CharField(null=True)
    first_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    first_warehouse_id = BigIntegerField(null=True)
    first_warehouse_name = CharField(constraints=[SQL("DEFAULT ''")])
    follow_time = DateTimeField(null=True)
    intercept_status = IntegerField(constraints=[SQL("DEFAULT 0")])
    intercept_time = DateTimeField(null=True)
    intercept_type = IntegerField(null=True)
    invalid_time = DateTimeField(null=True)
    issue_time = DateTimeField(null=True)
    labor_status = IntegerField(constraints=[SQL("DEFAULT 2")])
    labor_type = IntegerField(null=True)
    last_name = CharField(null=True)
    location_type = CharField(null=True)
    mobile_phone = CharField(null=True)
    order_id = BigAutoField()
    order_no = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    order_qty_type = IntegerField()
    order_status = IntegerField()
    order_type = IntegerField()
    pay_company = CharField(null=True)
    pay_time = DateTimeField(null=True)
    pay_type = CharField(null=True)
    platform_code = CharField(constraints=[SQL("DEFAULT ''")])
    platform_name = CharField(constraints=[SQL("DEFAULT ''")])
    postal_code = CharField(null=True)
    preemption_stock_no = CharField(null=True)
    province = CharField(null=True)
    province_name = CharField(null=True)
    receive_time = DateTimeField(null=True)
    relate_order_no = CharField(null=True)
    relate_sales_order_no = CharField(null=True)
    remark = CharField(constraints=[SQL("DEFAULT ''")])
    sales_order_remarks = CharField(null=True)
    sales_out_no = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sales_out_status = IntegerField(null=True)
    ship_type = IntegerField(null=True)
    site_code = CharField(constraints=[SQL("DEFAULT ''")])
    store_code = CharField(constraints=[SQL("DEFAULT ''")])
    store_name = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    update_user_id = BigIntegerField(null=True)
    urgent_status = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'oms_order'


class OmsOrderFollow(BaseModel):
    address = CharField(null=True)
    address1 = CharField(null=True)
    address2 = CharField(null=True)
    address3 = CharField(null=True)
    bom_version = CharField()
    buyer_id = CharField(null=True)
    buyer_name = CharField(null=True)
    city = CharField(null=True)
    country = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    delivery_warehouse_id = BigIntegerField()
    delivery_warehouse_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    email = CharField(null=True)
    eta = DateTimeField(null=True)
    follow_time = DateTimeField(null=True)
    id = BigAutoField()
    intercept_status = IntegerField(constraints=[SQL("DEFAULT 0")])
    intercept_type = IntegerField(null=True)
    item_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    labor_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    lack_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    logistics_actual = DecimalField(null=True)
    logistics_max = IntegerField(null=True)
    logistics_min = IntegerField(null=True)
    mobile_phone = CharField(null=True)
    order_eta = DateTimeField(null=True)
    order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    order_max_eta = DateTimeField(null=True)
    order_min_eta = DateTimeField(null=True)
    order_no = CharField()
    order_remark = CharField(null=True)
    order_status = IntegerField(null=True)
    pay_time = DateTimeField(null=True)
    platform_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    platform_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    postal_code = CharField(null=True)
    preempt_pre_on_way_qty = IntegerField()
    preempt_pre_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_plan_pre_qty = IntegerField()
    preempt_subscribe_plan_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_plan_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    province = CharField(null=True)
    purchase_order_pre_qty = IntegerField()
    purchase_order_qty = IntegerField()
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    relate_sales_order_no = CharField(null=True)
    sales_order_no = CharField()
    site_code = CharField(null=True)
    store_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    store_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)
    virtual_warehouse_code = CharField(null=True)
    virtual_warehouse_id = BigIntegerField(null=True)
    virtual_warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'oms_order_follow'


class OmsOrderFollowBak0113(BaseModel):
    address = CharField(null=True)
    address1 = CharField(null=True)
    address2 = CharField(null=True)
    address3 = CharField(null=True)
    buyer_id = CharField(null=True)
    buyer_name = CharField(null=True)
    city = CharField(null=True)
    country = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    delivery_warehouse_id = BigIntegerField()
    delivery_warehouse_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    email = CharField(null=True)
    eta = DateTimeField(null=True)
    id = BigAutoField()
    item_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    lack_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    mobile_phone = CharField(null=True)
    order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    order_no = CharField()
    pay_time = DateTimeField(null=True)
    platform_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    platform_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    postal_code = CharField(null=True)
    preempt_pre_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_plan_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_plan_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    province = CharField(null=True)
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    sales_order_no = CharField()
    site_code = CharField(null=True)
    store_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    store_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)

    class Meta:
        table_name = 'oms_order_follow_bak0113'


class OmsOrderFollowBak0320(BaseModel):
    address = CharField(null=True)
    address1 = CharField(null=True)
    address2 = CharField(null=True)
    address3 = CharField(null=True)
    buyer_id = CharField(null=True)
    buyer_name = CharField(null=True)
    city = CharField(null=True)
    country = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    delivery_warehouse_id = BigIntegerField()
    delivery_warehouse_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    email = CharField(null=True)
    eta = DateTimeField(null=True)
    id = BigAutoField()
    intercept_type = IntegerField(null=True)
    item_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    lack_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    mobile_phone = CharField(null=True)
    order_eta = DateTimeField(null=True)
    order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    order_no = CharField()
    pay_time = DateTimeField(null=True)
    platform_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    platform_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    postal_code = CharField(null=True)
    preempt_pre_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_plan_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_plan_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    province = CharField(null=True)
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    sales_order_no = CharField()
    site_code = CharField(null=True)
    store_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    store_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)

    class Meta:
        table_name = 'oms_order_follow_bak0320'


class OmsOrderFollowException(BaseModel):
    city = CharField(null=True)
    country = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_time = DateTimeField(null=True)
    id = BigAutoField()
    item_sku_code = CharField()
    item_status = IntegerField(null=True)
    order_eta = DateTimeField(null=True)
    pay_time = DateTimeField(null=True)
    platform_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    platform_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    postal_code = CharField(null=True)
    product_eta = DateTimeField(null=True)
    province = CharField(null=True)
    sales_order_no = CharField()
    site_code = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)

    class Meta:
        table_name = 'oms_order_follow_exception'
        indexes = (
            (('sales_order_no', 'item_sku_code'), True),
        )


class OmsOrderFollowExceptionDetail(BaseModel):
    bom_version = CharField(null=True)
    common_warehouse_code = CharField(null=True)
    common_warehouse_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_name = CharField(null=True)
    detail_item_id = IntegerField(null=True)
    exception_id = BigIntegerField(index=True)
    execute_overdue = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    follow_time = DateTimeField(null=True)
    id = BigAutoField()
    intercept_status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    labor_status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    max_eta = DateTimeField(null=True)
    min_eta = DateTimeField(null=True)
    oms_order_no = CharField()
    order_id = BigIntegerField()
    order_no = CharField(null=True)
    order_status = IntegerField()
    order_type = IntegerField(null=True)
    overdue_reason = CharField(null=True)
    qty = IntegerField()
    ship_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)
    warehouse_code = CharField(null=True)
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'oms_order_follow_exception_detail'


class OmsOrderFollowTrace(BaseModel):
    act_delivery_eta = DateField(null=True)
    act_overdue = IntegerField(null=True)
    city = CharField(null=True)
    country = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    expected_delivery_eta = DateField(null=True)
    expected_overdue = IntegerField(null=True)
    first_follow_result = UnknownField(null=True)  # json
    id = BigAutoField()
    item_sku_code = CharField()
    max_eta_days = IntegerField(null=True)
    max_product_eta_days = IntegerField(null=True)
    min_eta_days = IntegerField(null=True)
    min_expected_delivery_eta = DateField(null=True)
    min_product_eta = DateField(null=True)
    min_product_eta_days = IntegerField(null=True)
    order_type = IntegerField(null=True)
    pay_time = DateTimeField(null=True)
    platform_code = CharField(null=True)
    platform_name = CharField(null=True)
    postal_code = CharField(null=True)
    preempt_type = IntegerField(null=True)
    product_eta = DateField(null=True)
    province = CharField(null=True)
    sales_order_no = CharField()
    site_code = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)

    class Meta:
        table_name = 'oms_order_follow_trace'
        indexes = (
            (('sales_order_no', 'item_sku_code', 'del_flag'), True),
        )


class OmsOrderFollowTraceDetail(BaseModel):
    biz_no = CharField(null=True)
    bom_version = CharField(null=True)
    common_warehouse_code = CharField(null=True)
    common_warehouse_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    detail_item_id = IntegerField(null=True)
    eta = DateField()
    follow_time = DateTimeField()
    follow_trace_id = BigIntegerField(index=True)
    id = BigAutoField()
    in_warehouse_eta = DateField(null=True)
    in_warehouse_max_eta = DateField(null=True)
    in_warehouse_min_eta = DateField(null=True)
    intercept_status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    item_sku_code = CharField()
    labor_status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    latest_state = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    logistics_actual = DecimalField(null=True)
    logistics_max = IntegerField(null=True)
    logistics_min = IntegerField(null=True)
    max_eta = DateField()
    min_eta = DateField()
    oms_order_id = BigIntegerField()
    oms_order_no = CharField()
    oms_order_status = IntegerField()
    overdue_reason = CharField(null=True)
    overdue_state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    preempt_type = IntegerField()
    qty = IntegerField()
    remain_day = IntegerField(null=True)
    rollback_state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    rollback_time = DateTimeField(null=True)
    sales_order_no = CharField()
    shared_warehouse_code = CharField(null=True)
    shared_warehouse_name = CharField(null=True)
    ship_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    trace_key = CharField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    version = IntegerField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'oms_order_follow_trace_detail'


class OmsOrderItem(BaseModel):
    after_sales_attachment = UnknownField(null=True)  # json
    after_sales_remark = CharField(null=True)
    allot_no = CharField(null=True)
    allot_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    assign_issue_time = DateTimeField(null=True)
    attr_combined_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    clear_goods_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    cny_service_amount = DecimalField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_type = IntegerField(null=True)
    eta = DateTimeField(null=True)
    eta_info = UnknownField(null=True)  # json
    express_type = IntegerField(null=True)
    good_sku_code = CharField(null=True)
    id = BigAutoField()
    is_self_pick_up = IntegerField(null=True)
    issue_max_eta = DateTimeField(null=True)
    issue_min_eta = DateTimeField(null=True)
    issue_out_warehouse_max_eta = DateTimeField(null=True)
    issue_out_warehouse_min_eta = DateTimeField(null=True)
    item_category_id = BigIntegerField(null=True)
    item_category_name = CharField(null=True)
    item_currency_price = DecimalField()
    item_delivery_fee = DecimalField(null=True)
    item_delivery_fee_cny = DecimalField(null=True)
    item_delivery_fee_usd = DecimalField(null=True)
    item_dollar_price = DecimalField()
    item_pay_price = DecimalField()
    item_picture = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    item_price = DecimalField()
    item_purchase_price = DecimalField(null=True)
    item_sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    item_status = IntegerField(constraints=[SQL("DEFAULT 1")])
    item_tax = DecimalField(null=True)
    item_title = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    logistics_info = TextField(null=True)
    mall_label = UnknownField(null=True)  # json
    max_eta_days = IntegerField(null=True)
    min_eta = DateTimeField(null=True)
    min_eta_days = IntegerField(null=True)
    order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    package_info = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    purchase_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    receive_time = DateTimeField(null=True)
    sales_order_id = BigIntegerField()
    sales_order_item_id = BigIntegerField()
    sales_order_no = CharField(index=True)
    service_amount = DecimalField(null=True)
    source_info = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    supply_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    tag = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    usd_service_amount = DecimalField(null=True)
    warehouse_code = CharField(null=True)

    class Meta:
        table_name = 'oms_order_item'


class OmsOrderItemExt(BaseModel):
    bom_version = CharField(null=True)
    bom_version_assign_flag = IntegerField(constraints=[SQL("DEFAULT 2")])
    can_delivery_warehouse_json = UnknownField(null=True)  # json
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = CharField(constraints=[SQL("DEFAULT ''")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_qty = IntegerField()
    delivery_type = IntegerField(null=True)
    delivery_warehouse_assign_flag = IntegerField(constraints=[SQL("DEFAULT 2")], null=True)
    delivery_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(constraints=[SQL("DEFAULT ''")])
    express_type = IntegerField(null=True)
    good_sku_code = CharField(null=True)
    id = BigAutoField()
    item_sku_code = CharField()
    labor_message = CharField(null=True)
    labor_type = IntegerField(null=True)
    occupy_info = UnknownField(null=True)  # json
    order_id = BigIntegerField(index=True)
    order_item_id = BigIntegerField(index=True)
    purchase_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    transfer_no_list = UnknownField(null=True)  # json
    transfer_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    update_user_id = BigIntegerField(null=True)
    verify_order_complete_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    verify_order_result_json = UnknownField(null=True)  # json
    verify_order_result_max_eta = IntegerField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)
    warehouse_name = CharField(null=True)
    warehouse_sku_purchase_json = UnknownField(null=True)  # json

    class Meta:
        table_name = 'oms_order_item_ext'


class OmsOrderRelation(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    order_no = CharField(constraints=[SQL("DEFAULT ''")])
    sales_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    sales_order_no = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'oms_order_relation'


class OmsPlatformSkuSyncRule(BaseModel):
    create_time = DateTimeField(null=True)
    create_user = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    goods_sku_code = CharField(null=True)
    id = BigAutoField()
    platform_code = CharField()
    platform_name = CharField(null=True)
    platform_sku_code = CharField()
    platform_sku_item_id = CharField(null=True)
    rule_desc = CharField(null=True)
    rule_qty = IntegerField(null=True)
    store_code = CharField()
    store_name = CharField(null=True)
    success_sync_qty = IntegerField(null=True)
    sync_qty = IntegerField(null=True)
    sync_status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sync_time = DateTimeField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = CharField(null=True)
    update_user_id = IntegerField(null=True)
    valid_status = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = CharField(null=True)
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'oms_platform_sku_sync_rule'


class OmsPlatformStore(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = CharField(constraints=[SQL("DEFAULT ''")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    ext_info = TextField(null=True)
    id = BigAutoField()
    mapping_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    platform_code = CharField(constraints=[SQL("DEFAULT '0'")])
    platform_name = CharField(constraints=[SQL("DEFAULT '0'")])
    store_code = CharField(constraints=[SQL("DEFAULT ''")])
    store_name = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = CharField(constraints=[SQL("DEFAULT ''")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'oms_platform_store'
        indexes = (
            (('platform_code', 'store_code'), True),
        )


class OmsSalesOrder(BaseModel):
    address = CharField(null=True)
    address1 = CharField(null=True)
    address2 = CharField(null=True)
    address3 = CharField(null=True)
    audit_id = BigIntegerField(null=True)
    audit_name = CharField(null=True)
    audit_remarks = CharField(null=True)
    audit_start_time = DateTimeField(null=True)
    audit_status = IntegerField(null=True)
    audit_time = DateTimeField(null=True)
    buyer_id = CharField(null=True)
    buyer_name = CharField(null=True)
    cancel_delivery_time = DateTimeField(null=True)
    city = CharField(null=True)
    cny_service_amount = DecimalField(null=True)
    company = CharField(null=True)
    country = CharField(null=True)
    country_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user = CharField(null=True)
    create_user_id = BigIntegerField(null=True)
    credit_card_type = CharField(null=True)
    currency = CharField(null=True)
    currency_price = DecimalField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_fee = DecimalField(null=True)
    delivery_fee_cny = DecimalField(null=True)
    delivery_fee_usd = DecimalField(null=True)
    delivery_time = DateTimeField(null=True)
    delivery_time_end = CharField(null=True)
    delivery_time_start = CharField(null=True)
    discount_amount = DecimalField(null=True)
    dollar_price = DecimalField(null=True)
    email = CharField(null=True)
    ext_info = UnknownField(null=True)  # json
    first_name = CharField(null=True)
    has_reissue_order = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    intercept_time = DateTimeField(null=True)
    last_name = CharField(null=True)
    location_type = CharField(null=True)
    mobile_phone = CharField(null=True)
    no_pass_remarks = CharField(null=True)
    order_qty_type = IntegerField(null=True)
    order_source = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    order_type = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    pay_company = CharField(null=True)
    pay_no = CharField(null=True)
    pay_type = CharField(null=True)
    platform_code = CharField(null=True)
    platform_name = CharField(constraints=[SQL("DEFAULT ''")])
    postal_code = CharField(null=True)
    province = CharField(null=True)
    province_name = CharField(null=True)
    reissue_reason = CharField(null=True)
    relate_sales_order_no = CharField(null=True)
    responsible_party = CharField(null=True)
    sales_order_create_time = DateTimeField(null=True)
    sales_order_id = BigAutoField()
    sales_order_no = CharField(unique=True)
    sales_order_pay_price = DecimalField(null=True)
    sales_order_pay_time = DateTimeField(null=True)
    sales_order_price = DecimalField(null=True)
    sales_order_remarks = CharField(null=True)
    sales_order_status = IntegerField()
    sales_order_title = CharField(null=True)
    sales_order_update_time = DateTimeField(null=True)
    service_amount = DecimalField(null=True)
    site_code = CharField()
    store_code = CharField(null=True)
    store_name = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = CharField(null=True)
    update_user_id = BigIntegerField(null=True)
    usd_service_amount = DecimalField(null=True)

    class Meta:
        table_name = 'oms_sales_order'


class OmsSalesOrderItem(BaseModel):
    after_sales_attachment = UnknownField(null=True)  # json
    after_sales_remark = CharField(null=True)
    attr_combined_name = CharField(null=True)
    cancel_qty = IntegerField(null=True)
    cancel_qty_details = UnknownField(null=True)  # json
    clear_goods_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    cny_service_amount = DecimalField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_type = IntegerField(null=True)
    eta = DateTimeField(null=True)
    eta_info = UnknownField(null=True)  # json
    express_type = IntegerField(null=True)
    ext_info = UnknownField(null=True)  # json
    id = BigAutoField()
    is_self_pick_up = IntegerField(null=True)
    item_category_id = BigIntegerField(null=True)
    item_category_name = CharField(null=True)
    item_currency_price = DecimalField(null=True)
    item_delivery_fee = DecimalField(null=True)
    item_delivery_fee_cny = DecimalField(null=True)
    item_delivery_fee_usd = DecimalField(null=True)
    item_dollar_price = DecimalField(null=True)
    item_pay_price = DecimalField(null=True)
    item_picture = CharField(null=True)
    item_price = DecimalField(null=True)
    item_purchase_price = DecimalField(null=True)
    item_qty = IntegerField(null=True)
    item_sku_code = CharField(index=True, null=True)
    item_sku_id = BigIntegerField(null=True)
    item_sku_type = IntegerField(null=True)
    item_status = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    item_tax = DecimalField(null=True)
    item_title = CharField(null=True)
    mall_label = UnknownField(null=True)  # json
    max_eta_days = IntegerField(null=True)
    min_eta = DateTimeField(null=True)
    min_eta_days = IntegerField(null=True)
    origin_delivery_info = UnknownField(null=True)  # json
    package_info = CharField(null=True)
    problem_qty = IntegerField(null=True)
    sales_order_id = BigIntegerField(index=True)
    service_amount = DecimalField(null=True)
    source_info = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    supply_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    tag = CharField(null=True)
    update_time = DateTimeField(null=True)
    usd_service_amount = DecimalField(null=True)
    warehouse_code = CharField(null=True)

    class Meta:
        table_name = 'oms_sales_order_item'


class OmsSalesOrderLog(BaseModel):
    command_id = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    operate_content = UnknownField(null=True)  # json
    operate_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    operate_type = IntegerField(null=True)
    operator = CharField(null=True)
    operator_user_id = BigIntegerField(null=True)
    relate_order_no = UnknownField(null=True)  # json
    sales_order_id = BigIntegerField()
    sales_order_no = CharField()
    trace_id = CharField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'oms_sales_order_log'
        indexes = (
            (('sales_order_id', 'command_id'), False),
            (('sales_order_no', 'command_id'), False),
        )


class OmsSalesOrderOperateLog(BaseModel):
    content = TextField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    id = BigAutoField()
    operate_type = IntegerField(null=True)
    sales_order_id = BigIntegerField()
    source = CharField(null=True)
    trace_id = CharField(null=True)

    class Meta:
        table_name = 'oms_sales_order_operate_log'


class OmsSelfOrder(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    pick_up_order_no = CharField()
    push_mall_status = IntegerField(column_name='push_Mall_Status')
    push_robot_status = IntegerField(column_name='push_Robot_Status')
    sales_order_no = CharField()
    sku_code = CharField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'oms_self_order'


class OmsSkuRelation(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = CharField(constraints=[SQL("DEFAULT ''")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    platform_code = CharField(constraints=[SQL("DEFAULT '0'")])
    platform_name = CharField(constraints=[SQL("DEFAULT '0'")])
    platform_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sales_sku_json = CharField(null=True)
    store_code = CharField(constraints=[SQL("DEFAULT ''")])
    store_name = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = CharField(null=True)
    update_user_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'oms_sku_relation'
        indexes = (
            (('platform_sku_code', 'platform_code', 'store_code'), True),
        )


class OmsStockDistribute(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    delivery_warehouse_id = BigIntegerField()
    delivery_warehouse_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    id = BigAutoField()
    in_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    item_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    preempt_pre_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    prepare_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    stock_type = IntegerField(null=True)
    subscribe_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    subscribe_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    transfer_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    transfer_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)

    class Meta:
        table_name = 'oms_stock_distribute'


class OmsStockDistributeBak0113(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    delivery_warehouse_id = BigIntegerField()
    delivery_warehouse_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    id = BigAutoField()
    in_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    item_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    preempt_pre_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    prepare_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    stock_type = IntegerField(null=True)
    subscribe_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    subscribe_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    transfer_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    transfer_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)

    class Meta:
        table_name = 'oms_stock_distribute_bak0113'


class OmsStockDistributeBak0320(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    delivery_warehouse_id = BigIntegerField()
    delivery_warehouse_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    id = BigAutoField()
    in_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    item_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    preempt_pre_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_purchase_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_subscribe_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transfer_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    preempt_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    prepare_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    stock_type = IntegerField(null=True)
    subscribe_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    subscribe_transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    transfer_plan_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    transfer_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(index=True)

    class Meta:
        table_name = 'oms_stock_distribute_bak0320'


class OmsVirtualWarehouse(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    status = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = BigIntegerField()
    virtual_warehouse_code = CharField(unique=True)
    virtual_warehouse_name = CharField()

    class Meta:
        table_name = 'oms_virtual_warehouse'


class OmsVirtualWarehouseExt(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = BigIntegerField()
    virtual_warehouse_id = BigIntegerField(index=True)
    warehouse_code = CharField(unique=True)
    warehouse_id = BigIntegerField()
    warehouse_name = CharField()

    class Meta:
        table_name = 'oms_virtual_warehouse_ext'


class OmsWarehouseAllocationLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user = IntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    operation_description = TextField(null=True)
    operation_function = CharField(null=True)
    operation_result = CharField(null=True)
    rule_id = IntegerField(index=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = IntegerField(null=True)
    update_user_name = CharField(null=True)

    class Meta:
        table_name = 'oms_warehouse_allocation_log'


class OmsWarehouseDuration(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    data_version = IntegerField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    duration_max = IntegerField()
    duration_min = IntegerField()
    id = BigAutoField()
    postal_code = CharField()
    site_code = CharField()
    transport_type = IntegerField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    virtual_warehouse_code = CharField()
    virtual_warehouse_name = CharField()

    class Meta:
        table_name = 'oms_warehouse_duration'


class OmsWaresSkuReport(BaseModel):
    bad_stock = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    central_virtual_block = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    current_warehouse_name = CharField()
    current_warehouse_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_block = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    goods_sku_code = CharField(index=True)
    goods_stock = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    handle_date = CharField(null=True)
    id = BigAutoField()
    oms_block = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    other_block = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    purchase_order_stock = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    purchase_plan = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    purchase_stock = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    transfer_plan = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    transfer_stock = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    transit_stock = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(null=True)

    class Meta:
        table_name = 'oms_wares_sku_report'


class TdoDeliveryOrder(BaseModel):
    block_book_id = CharField(null=True)
    cancel_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    check_time = DateTimeField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT 0000-00-00 00:00:00")], index=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    currency = CharField(null=True)
    customer_remarks = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_order_code = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    end_handover_time = DateTimeField(null=True)
    express_state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    first_handover_time = DateTimeField(null=True)
    id = BigAutoField()
    intercept_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    logistics_remarks = CharField(null=True)
    operation_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    package_state = IntegerField(null=True)
    pick_time = DateTimeField(null=True)
    platform = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    platform_name = CharField(null=True)
    priority = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    prod_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    sale_amount = DecimalField(null=True)
    sale_order_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sale_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    sale_order_type = IntegerField(null=True)
    server_remarks = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    site = CharField(null=True)
    source_order_code = CharField(null=True)
    source_order_create_time = DateTimeField(null=True)
    source_transport_mode = IntegerField(constraints=[SQL("DEFAULT 0")])
    state = IntegerField(constraints=[SQL("DEFAULT 0")])
    stock_book_id = CharField(null=True)
    stock_out_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    store = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    store_name = CharField(null=True)
    transport_change_source = IntegerField(constraints=[SQL("DEFAULT 1")])
    transport_change_time = DateTimeField(null=True)
    transport_mode = IntegerField(constraints=[SQL("DEFAULT 1")])
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_code = CharField()
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'tdo_delivery_order'


class TdoDeliveryOrderDetail(BaseModel):
    bom_version = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_order_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    delivery_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    delivery_qty = IntegerField(null=True)
    height = DecimalField(null=True)
    id = BigAutoField()
    length = DecimalField(null=True)
    purchase_currency = CharField(null=True)
    purchase_price = DecimalField(null=True)
    sale_currency = CharField(null=True)
    sale_price = DecimalField(null=True)
    sale_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sale_sku_img = CharField(null=True)
    sale_sku_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    sale_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sku_id = BigIntegerField(null=True)
    sku_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    weight = DecimalField(null=True)
    width = DecimalField(null=True)

    class Meta:
        table_name = 'tdo_delivery_order_detail'


class TempOrder(BaseModel):
    order_no = CharField(constraints=[SQL("DEFAULT ''")])
    order_type = IntegerField()

    class Meta:
        table_name = 'temp_order'
        primary_key = False


class UndoLog(BaseModel):
    branch_id = BigIntegerField()
    context = CharField()
    id = BigAutoField()
    log_created = DateTimeField()
    log_modified = DateTimeField()
    log_status = IntegerField()
    rollback_info = TextField()
    xid = CharField()

    class Meta:
        table_name = 'undo_log'
        indexes = (
            (('xid', 'branch_id'), True),
        )


class WarehouseBomVersion(BaseModel):
    bom_version = CharField(null=True)
    good_sku_code = CharField(null=True)
    warehouse_sku_code = CharField(primary_key=True)

    class Meta:
        table_name = 'warehouse_bom_version'
