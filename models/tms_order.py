from peewee import *
from config import tms_db_config

database = MySQLDatabase('supply_logistics_order', **tms_db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class FlywaySchemaHistory(BaseModel):
    checksum = IntegerField(null=True)
    description = CharField()
    execution_time = IntegerField()
    installed_by = CharField()
    installed_on = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    installed_rank = AutoField()
    script = CharField()
    success = IntegerField(index=True)
    type = CharField()
    version = CharField(null=True)

    class Meta:
        table_name = 'flyway_schema_history'


class LogisticsAfterSalesClaim(BaseModel):
    after_sales_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    after_sales_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    claim_bill_account = CharField(null=True)
    claim_bill_amount = DecimalField(null=True)
    claim_bill_currency = IntegerField(null=True)
    claim_bill_date = DateTimeField(null=True)
    claim_bill_oa = CharField(null=True)
    claim_bill_oa_time = DateTimeField(null=True)
    claim_bill_remark = CharField(null=True)
    claim_bill_time = DateTimeField(null=True)
    claim_bill_type_code = CharField(null=True)
    claim_bill_type_name = CharField(null=True)
    claim_bill_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    claim_bill_username = CharField(constraints=[SQL("DEFAULT ''")])
    claim_launch_amount = DecimalField(null=True)
    claim_launch_currency = IntegerField(null=True)
    claim_launch_date = DateTimeField(null=True)
    claim_launch_remark = CharField(null=True)
    claim_launch_time = DateTimeField(null=True)
    claim_launch_type_code = CharField(null=True)
    claim_launch_type_name = CharField(null=True)
    claim_launch_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    claim_launch_username = CharField(constraints=[SQL("DEFAULT ''")])
    claim_result_amount = DecimalField(null=True)
    claim_result_currency = IntegerField(null=True)
    claim_result_date = DateTimeField(null=True)
    claim_result_reason_code = CharField(null=True)
    claim_result_reason_name = CharField(null=True)
    claim_result_remark = CharField(null=True)
    claim_result_time = DateTimeField(null=True)
    claim_result_type = IntegerField(null=True)
    claim_result_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    claim_result_username = CharField(constraints=[SQL("DEFAULT ''")])
    claim_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    express_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    express_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_after_sales_claim'


class LogisticsAfterSalesOrder(BaseModel):
    after_sale_no = CharField(null=True)
    after_sales_amount = DecimalField(null=True)
    after_sales_currency = IntegerField(null=True)
    after_sales_desc = CharField(null=True)
    after_sales_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    after_sales_order_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    after_sales_reason_code = CharField(null=True)
    after_sales_reason_name = CharField(null=True)
    after_sales_value_amount = DecimalField(null=True)
    after_sales_value_currency = IntegerField(null=True)
    audit_reason_code = CharField(null=True)
    audit_reason_name = CharField(null=True)
    audit_remark = CharField(null=True)
    audit_time = DateTimeField(null=True)
    audit_type = IntegerField(null=True)
    audit_user_id = BigIntegerField(null=True)
    audit_username = CharField(null=True)
    confirm_amount = DecimalField(null=True)
    confirm_currency = IntegerField(null=True)
    confirm_reason_code = CharField(null=True)
    confirm_reason_name = CharField(null=True)
    confirm_remark = CharField(null=True)
    confirm_time = DateTimeField(null=True)
    confirm_type = IntegerField(null=True)
    confirm_user_id = BigIntegerField(null=True)
    confirm_username = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    customer_id = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_time = DateTimeField(null=True)
    express_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    express_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    in_claim_standards = IntegerField(null=True)
    not_suitable_claim_standard_reason = CharField(null=True)
    order_code = CharField(constraints=[SQL("DEFAULT ''")])
    order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    package_code = CharField(constraints=[SQL("DEFAULT ''")])
    package_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_amount = DecimalField(null=True)
    purchase_amount_currency = IntegerField(null=True)
    sales_amount = DecimalField(null=True)
    sales_amount_currency = IntegerField(null=True)
    tracking_state = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_after_sales_order'


class LogisticsAfterSalesReasonCredential(BaseModel):
    after_sales_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    after_sales_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    file_name = CharField(constraints=[SQL("DEFAULT ''")])
    file_path = CharField(constraints=[SQL("DEFAULT ''")])
    file_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_after_sales_reason_credential'


class LogisticsExpressOperationLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    express_order_id = BigIntegerField(null=True)
    id = BigAutoField()
    operation_log_content = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    operation_log_ip = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    operation_log_node = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    operation_log_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    operation_log_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    operation_log_user_username = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    trace_id = CharField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_express_operation_log'
        indexes = (
            (('del_flag', 'express_order_id'), False),
        )


class LogisticsExpressOrder(BaseModel):
    barcode = CharField(constraints=[SQL("DEFAULT ''")])
    cancel_apply_time = DateTimeField(null=True)
    cancel_reason = IntegerField(null=True)
    cancel_state = IntegerField(null=True)
    cancel_time = DateTimeField(null=True)
    cancel_type = IntegerField(null=True)
    channel_code = CharField(constraints=[SQL("DEFAULT ''")])
    channel_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    channel_name = CharField(constraints=[SQL("DEFAULT ''")])
    channel_order_code = CharField(null=True)
    channel_order_ext = UnknownField(null=True)  # json
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    express_order_code = CharField(null=True)
    express_order_source = IntegerField(constraints=[SQL("DEFAULT 0")])
    express_order_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    logistics_brand = CharField(constraints=[SQL("DEFAULT ''")])
    logistics_service = CharField(constraints=[SQL("DEFAULT ''")])
    package_code = CharField(constraints=[SQL("DEFAULT ''")])
    package_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    product_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    product_name = CharField(constraints=[SQL("DEFAULT ''")])
    service_code = CharField(constraints=[SQL("DEFAULT ''")])
    tracking_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    transfer_order_code = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'logistics_express_order'
        indexes = (
            (('package_code', 'del_flag'), False),
            (('package_id', 'del_flag'), False),
            (('package_id', 'del_flag'), False),
        )


class LogisticsExpressOrderFile(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    express_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    express_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    file_format = CharField(null=True)
    file_path = CharField(constraints=[SQL("DEFAULT ''")])
    file_scale = CharField(constraints=[SQL("DEFAULT ''")])
    file_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    print_copies = IntegerField(null=True)
    print_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    print_direction = IntegerField(constraints=[SQL("DEFAULT 0")])
    source_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_express_order_file'
        indexes = (
            (('express_order_id', 'del_flag'), False),
        )


class LogisticsOrder(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    customer_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    order_category = IntegerField(null=True)
    order_code = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    order_source = IntegerField(constraints=[SQL("DEFAULT 0")])
    order_unique_id = CharField(constraints=[SQL("DEFAULT ''")])
    payment_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    payment_state_remark = IntegerField(null=True)
    payment_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    platform = CharField(constraints=[SQL("DEFAULT ''")])
    source_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    source_order_remark = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_order'


class LogisticsOrderAddress(BaseModel):
    address = CharField(constraints=[SQL("DEFAULT ''")])
    address2 = CharField(null=True)
    address3 = CharField(null=True)
    address_attribute = IntegerField(constraints=[SQL("DEFAULT 0")])
    address_code = CharField(null=True)
    address_id = BigIntegerField(null=True)
    address_name = CharField(null=True)
    address_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    city_code = CharField(constraints=[SQL("DEFAULT ''")])
    city_name = CharField(constraints=[SQL("DEFAULT ''")])
    company_name = CharField(null=True)
    country_code = CharField(constraints=[SQL("DEFAULT ''")])
    country_name = CharField(constraints=[SQL("DEFAULT ''")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    email = CharField(constraints=[SQL("DEFAULT ''")])
    first_name = CharField(constraints=[SQL("DEFAULT ''")])
    id = BigAutoField()
    last_name = CharField(constraints=[SQL("DEFAULT ''")])
    order_code = CharField(constraints=[SQL("DEFAULT ''")])
    order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    phone = CharField(constraints=[SQL("DEFAULT ''")])
    postcode = CharField(constraints=[SQL("DEFAULT ''")])
    province_code = CharField(constraints=[SQL("DEFAULT ''")])
    province_name = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_order_address'
        indexes = (
            (('order_id', 'del_flag'), False),
        )


class LogisticsOrderExtension(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_begin_time = CharField(null=True)
    delivery_end_time = CharField(null=True)
    delivery_ware_code = CharField(null=True)
    id = BigAutoField()
    insure_goods_amount = DecimalField(null=True)
    insure_goods_category = CharField(null=True)
    insure_goods_currency = IntegerField(null=True)
    order_code = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    pick_up_begin_time = CharField(null=True)
    pick_up_end_time = CharField(null=True)
    pick_up_time = DateTimeField(null=True)
    source_platform_code = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_order_extension'
        indexes = (
            (('order_id', 'del_flag'), False),
        )


class LogisticsOrderTag(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    order_code = CharField(constraints=[SQL("DEFAULT ''")])
    order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    property_key = CharField(constraints=[SQL("DEFAULT ''")])
    property_value = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_order_tag'
        indexes = (
            (('order_id', 'del_flag'), False),
        )


class LogisticsPackage(BaseModel):
    cancel_time = DateTimeField(null=True)
    channel_transport_type = IntegerField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_time = DateTimeField(null=True)
    id = BigAutoField()
    order_code = CharField(constraints=[SQL("DEFAULT ''")])
    order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    order_number = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    package_code = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    package_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    package_state_reason = IntegerField(null=True)
    package_state_remark = CharField(null=True)
    payment_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    source_package_code = CharField(constraints=[SQL("DEFAULT ''")])
    source_type = IntegerField(null=True)
    transport_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    trial_code = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'logistics_package'


class LogisticsPackageChannel(BaseModel):
    account_no = CharField(constraints=[SQL("DEFAULT ''")])
    channel_code = CharField(constraints=[SQL("DEFAULT ''")])
    channel_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    channel_name = CharField(constraints=[SQL("DEFAULT ''")])
    channel_zone_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    express_order_source = IntegerField(null=True)
    id = BigAutoField()
    logistics_brand = CharField(constraints=[SQL("DEFAULT ''")])
    logistics_service = CharField(constraints=[SQL("DEFAULT ''")])
    package_code = CharField(constraints=[SQL("DEFAULT ''")])
    package_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    product_billing_rule_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    product_discount_rule_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    product_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    product_name = CharField(constraints=[SQL("DEFAULT ''")])
    service_code = CharField(constraints=[SQL("DEFAULT ''")])
    source_channel_code = CharField(constraints=[SQL("DEFAULT ''")])
    source_channel_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    source_channel_name = CharField(constraints=[SQL("DEFAULT ''")])
    source_channel_zone_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    source_logistics_brand = CharField(constraints=[SQL("DEFAULT ''")])
    source_logistics_service = CharField(constraints=[SQL("DEFAULT ''")])
    source_service_code = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_package_channel'
        indexes = (
            (('package_code', 'del_flag'), True),
        )


class LogisticsPackageCollection(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    declare_amount = DecimalField(null=True)
    declare_currency = IntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    goods_category_code = CharField(constraints=[SQL("DEFAULT ''")])
    goods_category_name = CharField(constraints=[SQL("DEFAULT ''")])
    goods_desc = CharField(constraints=[SQL("DEFAULT ''")])
    height = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    id = BigAutoField()
    length = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    package_code = CharField(constraints=[SQL("DEFAULT ''")])
    package_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    size_unit = CharField(constraints=[SQL("DEFAULT ''")])
    tray_name = CharField(null=True)
    truck_class = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])
    weight = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    weight_unit = CharField(constraints=[SQL("DEFAULT ''")])
    width = DecimalField(constraints=[SQL("DEFAULT 0.000000")])

    class Meta:
        table_name = 'logistics_package_collection'
        indexes = (
            (('package_id', 'del_flag'), False),
        )


class LogisticsPackageCollectionDetail(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    customs_code = CharField(constraints=[SQL("DEFAULT ''")])
    declare_currency = CharField(null=True)
    declare_price = DecimalField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    goods_code = CharField(constraints=[SQL("DEFAULT ''")])
    goods_name = CharField(constraints=[SQL("DEFAULT ''")])
    height = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    id = BigAutoField()
    length = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    package_code = CharField(constraints=[SQL("DEFAULT ''")])
    package_detail_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    package_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    product_name_en = CharField(null=True)
    product_name_zh = CharField(null=True)
    purchase_currency = CharField(null=True)
    purchase_price_amount = DecimalField(null=True)
    qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    sale_currency = CharField(null=True)
    sale_price_amount = DecimalField(null=True)
    size_unit = CharField(constraints=[SQL("DEFAULT ''")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])
    weight = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    weight_unit = CharField(constraints=[SQL("DEFAULT ''")])
    width = DecimalField(constraints=[SQL("DEFAULT 0.000000")])

    class Meta:
        table_name = 'logistics_package_collection_detail'
        indexes = (
            (('package_detail_id', 'del_flag'), False),
            (('package_id', 'del_flag'), False),
        )


class LogisticsPackageExtension(BaseModel):
    add_service = CharField(null=True)
    back_reason = CharField(null=True)
    bill_id = BigIntegerField(null=True)
    bill_tray_qty = IntegerField(null=True)
    cancel_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    channel_unit = IntegerField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    cutoff_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    fault_person = IntegerField(null=True)
    height = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    id = BigAutoField()
    increase_service = CharField(null=True)
    intercept_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    length = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    order_info = UnknownField(null=True)  # json
    package_code = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    package_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    pick_code = CharField(null=True)
    proof_url = CharField(null=True)
    refund_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    risk_info = UnknownField(null=True)  # json
    risk_remark = CharField(constraints=[SQL("DEFAULT ''")])
    risk_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    sale_code = CharField(null=True)
    size_unit = CharField(constraints=[SQL("DEFAULT ''")])
    trial_info = UnknownField(null=True)  # json
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])
    volume_coefficient = DecimalField(null=True)
    weight = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    weight_unit = CharField(constraints=[SQL("DEFAULT ''")])
    width = DecimalField(constraints=[SQL("DEFAULT 0.000000")])

    class Meta:
        table_name = 'logistics_package_extension'
        indexes = (
            (('package_id', 'del_flag'), False),
        )


class LogisticsPackageFeeItem(BaseModel):
    cost_price_amount = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    cost_price_currency = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    discount_amount = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    discount_currency = IntegerField(constraints=[SQL("DEFAULT 0")])
    discount_rate = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    fee_item_code = CharField(constraints=[SQL("DEFAULT ''")])
    fee_item_name = CharField(constraints=[SQL("DEFAULT ''")])
    id = BigAutoField()
    increase_rate = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    package_code = CharField(constraints=[SQL("DEFAULT ''")])
    package_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    sale_price_amount = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    sale_price_currency = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_package_fee_item'
        indexes = (
            (('package_id', 'del_flag'), False),
        )


class LogisticsPackageOperationLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    operation_log_content = CharField(constraints=[SQL("DEFAULT ''")])
    operation_log_ip = CharField(constraints=[SQL("DEFAULT ''")])
    operation_log_node = IntegerField(constraints=[SQL("DEFAULT 0")])
    operation_log_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    operation_log_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    operation_log_user_username = CharField(constraints=[SQL("DEFAULT ''")])
    package_code = CharField(constraints=[SQL("DEFAULT ''")])
    trace_id = CharField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'logistics_package_operation_log'
