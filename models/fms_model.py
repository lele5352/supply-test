from peewee import *
from config import scms_db_config

database = MySQLDatabase('supply_fms', **scms_db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class ChannelBill(BaseModel):
    bill_code = CharField(unique=True)
    bill_date_end = DateField()
    bill_date_start = DateField()
    bill_type = IntegerField()
    channel_amount = DecimalField(null=True)
    channel_amount_currency = CharField(null=True)
    channel_bill_no = CharField(index=True)
    channel_bill_remark = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    detail_upload_status = IntegerField()
    difference_amount = DecimalField(null=True)
    difference_amount_currency = CharField(null=True)
    difference_amount_ratio = DecimalField(null=True)
    expect_amount = DecimalField(null=True)
    expect_amount_currency = CharField(null=True)
    fee_item_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    receive_bill_date = DateField()
    reconciliation_status = IntegerField()
    service_provider = CharField(index=True)
    settlement_amount = DecimalField(null=True)
    settlement_amount_currency = CharField(null=True)
    settlement_status = IntegerField()
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'channel_bill'


class ChannelBillBackup(BaseModel):
    bill_code = CharField()
    bill_date_end = DateField()
    bill_date_start = DateField()
    bill_type = IntegerField()
    channel_amount = DecimalField(null=True)
    channel_amount_currency = CharField(null=True)
    channel_bill_no = CharField()
    channel_bill_remark = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    detail_upload_status = IntegerField()
    difference_amount = DecimalField(null=True)
    difference_amount_currency = CharField(null=True)
    difference_amount_ratio = DecimalField(null=True)
    expect_amount = DecimalField(null=True)
    expect_amount_currency = CharField(null=True)
    fee_item_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigIntegerField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    receive_bill_date = DateField()
    reconciliation_status = IntegerField()
    service_provider = CharField()
    settlement_amount = DecimalField(null=True)
    settlement_amount_currency = CharField(null=True)
    settlement_status = IntegerField()
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'channel_bill_backup'
        primary_key = False


class ChannelBillDetail(BaseModel):
    arrival_time = DateField(null=True)
    bill_exception_type = IntegerField()
    channel = CharField(null=True)
    channel_amount = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    channel_amount_currency = CharField()
    channel_bill_id = BigIntegerField(index=True)
    channel_weight = DecimalField(null=True)
    channel_weight_unit = CharField(null=True)
    commit_time = DateTimeField(null=True)
    commit_user_id = BigIntegerField(null=True)
    commit_user_name = CharField(null=True)
    confirm_time = DateTimeField(null=True)
    confirm_user_id = BigIntegerField(null=True)
    confirm_user_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_user_name = CharField(null=True)
    declare_customs_amount = DecimalField(null=True)
    declare_customs_amount_currency = CharField(null=True)
    destination = CharField(null=True)
    detail_reconciliation_status = IntegerField(constraints=[SQL("DEFAULT 0")])
    detail_settlement_status = IntegerField(constraints=[SQL("DEFAULT 0")])
    difference_amount = DecimalField(null=True)
    difference_amount_currency = CharField(null=True)
    difference_amount_ratio = DecimalField(null=True)
    difference_weight = DecimalField(null=True)
    difference_weight_ratio = DecimalField(null=True)
    difference_weight_unit = CharField(null=True)
    dispatch_place = CharField(null=True)
    exception_confirm_reason = CharField(null=True)
    expect_amount = DecimalField(null=True)
    expect_amount_currency = CharField(null=True)
    expect_fee_item_id = BigIntegerField(null=True)
    expect_weight = DecimalField(null=True)
    expect_weight_unit = CharField(null=True)
    fee_item_category = IntegerField()
    fee_item_name = CharField(index=True)
    fee_item_type = IntegerField()
    freight_no = CharField(index=True)
    goods_amount = DecimalField(null=True)
    goods_amount_currency = CharField(null=True)
    history_settlement_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    import_time = DateTimeField(null=True)
    is_amount_updated = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    not_delivered = IntegerField(constraints=[SQL("DEFAULT 0")])
    platform = CharField(null=True)
    postcode = CharField(null=True)
    province_code = CharField(null=True)
    reject_remark = CharField(null=True)
    sales_amount = DecimalField(null=True)
    sales_amount_currency = CharField(null=True)
    sales_no = CharField(null=True)
    service_provider = CharField()
    settlement_amount = DecimalField(null=True)
    settlement_amount_currency = CharField(null=True)
    settlement_weight = DecimalField(null=True)
    settlement_weight_unit = CharField(null=True)
    shipping_date = DateField(null=True)
    shipping_warehouse = CharField(null=True)
    site = CharField(null=True)
    store = CharField(null=True)
    trace_id = CharField(null=True)
    transaction_type = IntegerField(null=True)
    transport_stage = IntegerField()
    transport_type = IntegerField(null=True)
    uk = CharField(index=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'channel_bill_detail'


class ChannelBillDetailAttachment(BaseModel):
    attachment_url = CharField()
    bill_detail_id = BigIntegerField(index=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'channel_bill_detail_attachment'


class ChannelBillDetailSourceNo(BaseModel):
    bill_detail_id = BigIntegerField(index=True)
    container_no = CharField(index=True, null=True)
    entry_no = CharField(null=True)
    id = BigAutoField()
    invoice_no = CharField(null=True)
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    out_stock_no = CharField(index=True, null=True)
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'channel_bill_detail_source_no'


class CurrencyRate(BaseModel):
    base_currency_code = CharField()
    belong_time = DateTimeField()
    create_time = DateTimeField()
    current_rate = DecimalField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    to_currency_code = CharField()
    trace_id = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'currency_rate'


class ExcelImportTask(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    fail_num = IntegerField(null=True)
    finish_time = DateTimeField(null=True)
    id = BigAutoField()
    import_result = UnknownField(null=True)  # json
    import_status = IntegerField()
    import_type = IntegerField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    success_num = IntegerField(null=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'excel_import_task'


class ExpectFeeItem(BaseModel):
    arrival_time = DateField(null=True)
    channel = CharField()
    charged_weight_kg = DecimalField(null=True)
    charged_weight_lbs = DecimalField(null=True)
    check_bill_time = DateTimeField(null=True)
    check_bill_user_id = BigIntegerField(null=True)
    check_bill_user_name = CharField(null=True)
    confirm_time = DateTimeField(null=True)
    confirm_user_id = BigIntegerField(null=True)
    confirm_user_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    declare_customs_amount = DecimalField(null=True)
    declare_customs_amount_currency = CharField(null=True)
    delivery_no = CharField(index=True)
    destination = CharField(null=True)
    expect_amount = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    expect_amount_currency = CharField()
    expect_amount_usd = DecimalField(null=True)
    expect_fee_item_status = IntegerField()
    expect_type = IntegerField()
    fee_item_category = IntegerField()
    fee_item_name = CharField()
    fee_item_type = IntegerField()
    goods_amount = DecimalField(null=True)
    goods_amount_currency = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    platform = CharField(null=True)
    post_code = CharField(null=True)
    province_code = CharField(null=True)
    remark = CharField(null=True)
    sales_amount = DecimalField(null=True)
    sales_amount_currency = CharField(null=True)
    servicer = CharField(index=True)
    shipping_place = CharField(null=True)
    shipping_time = DateField(index=True)
    shipping_warehouse = CharField(null=True)
    site = CharField(null=True)
    store = CharField(null=True)
    trace_id = CharField(null=True)
    transaction_type = IntegerField()
    transport_part = IntegerField()
    transport_type = IntegerField()
    uk = CharField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'expect_fee_item'
        indexes = (
            (('uk', 'create_time', 'is_deleted'), True),
        )


class ExpectFeeItemDetail(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField(null=True)
    create_user_name = CharField(null=True)
    expect_fee_item_id = BigIntegerField(index=True)
    high = DecimalField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    length = DecimalField(null=True)
    out_stock_no = CharField(index=True, null=True)
    package_no = CharField(index=True, null=True)
    sales_no = CharField(null=True)
    size_unit = CharField(null=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    version = IntegerField(null=True)
    weight = DecimalField(null=True)
    weight_unit = CharField(null=True)
    width = DecimalField(null=True)

    class Meta:
        table_name = 'expect_fee_item_detail'


class ExpectFeeItemSku(BaseModel):
    expect_fee_item_detail_id = BigIntegerField(index=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    package_detail = UnknownField(null=True)  # json
    sku_code = CharField(index=True, null=True)
    sku_name = CharField(null=True)
    sku_type = CharField(null=True)
    trace_id = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'expect_fee_item_sku'


class FeeItem(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    fee_item_category = IntegerField()
    fee_item_name = CharField(unique=True)
    fee_item_type = IntegerField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    remark = CharField(null=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(null=True)

    class Meta:
        table_name = 'fee_item'


class FeeRate(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    rate_date = DateField(null=True, unique=True)
    remark = CharField(null=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'fee_rate'


class FeeRateDetail(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    fee_rate_id = BigIntegerField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    rate = DecimalField()
    rate_date = DateField(null=True)
    servicer = CharField()
    trace_id = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'fee_rate_detail'
        indexes = (
            (('servicer', 'fee_rate_id', 'is_deleted'), True),
        )


class LogisticsSettle(BaseModel):
    bill_no = CharField(index=True)
    bill_remark = CharField(null=True)
    bill_type = IntegerField()
    channel_amount = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    channel_amount_currency = CharField()
    channel_bill_no = CharField(index=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    different_amount = DecimalField(null=True)
    different_amount_currency = CharField(null=True)
    different_ratio = DecimalField(null=True)
    expect_amount = DecimalField(null=True)
    expect_amount_currency = CharField(null=True)
    fee_item_count = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    logistics_settle_status = IntegerField()
    oa_no = CharField(null=True)
    reject_remark = CharField(null=True)
    reject_time = DateTimeField(null=True)
    reject_user_id = BigIntegerField(null=True)
    reject_user_name = CharField(null=True)
    servicer = CharField(index=True)
    settle_amount = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    settle_amount_currency = CharField()
    settle_no = CharField(unique=True)
    settle_time = DateTimeField(null=True)
    settle_user_id = BigIntegerField(null=True)
    settle_user_name = CharField(null=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(null=True)

    class Meta:
        table_name = 'logistics_settle'


class LogisticsSettleDetail(BaseModel):
    arrival_time = DateField(null=True)
    bill_detail_id = BigIntegerField(index=True)
    bill_id = BigIntegerField(index=True)
    channel_amount = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    channel_amount_currency = CharField()
    declare_customs_amount = DecimalField(null=True)
    declare_customs_amount_currency = CharField(null=True)
    delivery_no = CharField(index=True)
    destination = CharField(null=True)
    exception_confirm_remark = CharField(null=True)
    expect_amount = DecimalField(null=True)
    expect_amount_currency = CharField(null=True)
    fee_item_category = IntegerField(null=True)
    fee_item_name = CharField()
    fee_item_type = IntegerField(null=True)
    goods_amount = DecimalField(null=True)
    goods_amount_currency = CharField(null=True)
    history_settle_amount = DecimalField(null=True)
    history_settle_amount_currency = CharField(null=True)
    history_settle_count = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    logistics_settle_id = BigIntegerField(index=True)
    platform = CharField(null=True)
    sales_amount = DecimalField(null=True)
    sales_amount_currency = CharField(null=True)
    sales_no = CharField(null=True)
    service_provider = CharField()
    settle_amount = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    settle_amount_currency = CharField()
    shipping_place = CharField(null=True)
    shipping_time = DateField(null=True)
    shipping_warehouse = CharField(null=True)
    site = CharField(null=True)
    store = CharField(null=True)
    trace_id = CharField(null=True)
    transaction_type = IntegerField(null=True)
    transport_part = IntegerField()
    transport_type = IntegerField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'logistics_settle_detail'


class LogisticsSettleDetailSource(BaseModel):
    entry_no = CharField(null=True)
    id = BigAutoField()
    invoice_no = CharField(null=True)
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    logistics_settle_detail_id = BigIntegerField(index=True)
    out_stock_no = CharField(index=True, null=True)
    package_no = CharField(index=True, null=True)
    trace_id = CharField(null=True)

    class Meta:
        table_name = 'logistics_settle_detail_source'


class VerificationDetail(BaseModel):
    arrival_time = DateField(null=True)
    bill_code = CharField(null=True)
    bill_detail_id = BigIntegerField(index=True, null=True)
    bill_id = BigIntegerField(index=True, null=True)
    channel_amount_original = DecimalField(constraints=[SQL("DEFAULT 0.000000")])
    channel_amount_original_currency = CharField()
    channel_amount_usd = DecimalField()
    channel_amount_usd_currency = CharField()
    declare_customs_amount = DecimalField(null=True)
    declare_customs_amount_currency = CharField(null=True)
    delivery_no = CharField(null=True)
    destination = CharField(null=True)
    dispatch_place = CharField(null=True)
    expect_amount_original = DecimalField(null=True)
    expect_amount_original_currency = CharField(null=True)
    expect_amount_usd = DecimalField(null=True)
    expect_amount_usd_currency = CharField(null=True)
    fee_item_category = IntegerField()
    fee_item_name = CharField(index=True)
    fee_item_type = IntegerField()
    goods_amount = DecimalField(null=True)
    goods_amount_currency = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    platform = CharField(null=True)
    sales_amount = DecimalField(null=True)
    sales_amount_currency = CharField(null=True)
    service_provider = CharField()
    settle_detail_id = BigIntegerField(index=True, null=True)
    settle_id = BigIntegerField(index=True, null=True)
    settle_no = CharField(null=True)
    settlement_amount_original = DecimalField()
    settlement_amount_original_currency = CharField()
    settlement_amount_usd = DecimalField()
    settlement_amount_usd_currency = CharField()
    shipping_date = DateField(null=True)
    shipping_warehouse = CharField(null=True)
    site = CharField(null=True)
    store = CharField(null=True)
    trace_id = CharField(null=True)
    transaction_type = IntegerField(null=True)
    transport_stage = IntegerField(null=True)
    transport_type = IntegerField(null=True)
    verification_id = BigIntegerField(index=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'verification_detail'


class VerificationDetailSourceNo(BaseModel):
    entry_no = CharField(null=True)
    id = BigAutoField()
    invoice_no = CharField(null=True)
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    out_stock_no = CharField(null=True)
    sales_no = CharField(null=True)
    trace_id = CharField(null=True)
    verification_detail_id = BigIntegerField(index=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'verification_detail_source_no'


class VerificationInfo(BaseModel):
    bill_type = IntegerField()
    channel_amount_original = DecimalField()
    channel_amount_original_currency = CharField()
    channel_amount_usd = DecimalField()
    channel_amount_usd_currency = CharField()
    channel_normal_amount_original = DecimalField()
    channel_normal_amount_original_currency = CharField()
    channel_normal_amount_usd = DecimalField()
    channel_normal_amount_usd_currency = CharField()
    channel_tariff_amount_original = DecimalField()
    channel_tariff_amount_original_currency = CharField()
    channel_tariff_amount_usd = DecimalField()
    channel_tariff_amount_usd_currency = CharField()
    complete_settlement_time = DateTimeField()
    container_no = CharField(index=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    difference_amount_original = DecimalField(null=True)
    difference_amount_original_currency = CharField(null=True)
    difference_amount_original_ratio = DecimalField(null=True)
    difference_amount_usd = DecimalField(null=True)
    difference_amount_usd_currency = CharField(null=True)
    difference_amount_usd_ratio = DecimalField(null=True)
    difference_normal_amount_original = DecimalField(null=True)
    difference_normal_amount_original_currency = CharField(null=True)
    difference_normal_amount_original_ratio = DecimalField(null=True)
    difference_normal_amount_usd = DecimalField(null=True)
    difference_normal_amount_usd_currency = CharField(null=True)
    difference_normal_amount_usd_ratio = DecimalField(null=True)
    difference_tariff_amount_original = DecimalField(null=True)
    difference_tariff_amount_original_currency = CharField(null=True)
    difference_tariff_amount_original_ratio = DecimalField(null=True)
    difference_tariff_amount_usd = DecimalField(null=True)
    difference_tariff_amount_usd_currency = CharField(null=True)
    difference_tariff_amount_usd_ratio = DecimalField(null=True)
    expect_amount_original = DecimalField(null=True)
    expect_amount_original_currency = CharField(null=True)
    expect_amount_usd = DecimalField(null=True)
    expect_amount_usd_currency = CharField(null=True)
    expect_normal_amount_original = DecimalField(null=True)
    expect_normal_amount_original_currency = CharField(null=True)
    expect_normal_amount_usd = DecimalField(null=True)
    expect_normal_amount_usd_currency = CharField(null=True)
    expect_tariff_amount_original = DecimalField(null=True)
    expect_tariff_amount_original_currency = CharField(null=True)
    expect_tariff_amount_usd = DecimalField(null=True)
    expect_tariff_amount_usd_currency = CharField(null=True)
    fee_item_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    settlement_amount_original = DecimalField()
    settlement_amount_original_currency = CharField()
    settlement_amount_usd = DecimalField()
    settlement_amount_usd_currency = CharField()
    settlement_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    settlement_normal_amount_original = DecimalField()
    settlement_normal_amount_original_currency = CharField()
    settlement_normal_amount_usd = DecimalField()
    settlement_normal_amount_usd_currency = CharField()
    settlement_tariff_amount_original = DecimalField()
    settlement_tariff_amount_original_currency = CharField()
    settlement_tariff_amount_usd = DecimalField()
    settlement_tariff_amount_usd_currency = CharField()
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    verification_no = CharField(unique=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'verification_info'


class VerificationSourceNo(BaseModel):
    bill_code = CharField(index=True, null=True)
    bill_id = BigIntegerField(index=True, null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    oa_no = CharField(index=True, null=True)
    service_provider = CharField(index=True, null=True)
    settle_id = BigIntegerField(index=True, null=True)
    settle_no = CharField(index=True, null=True)
    trace_id = CharField(null=True)
    verification_info_id = BigIntegerField(index=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'verification_source_no'
