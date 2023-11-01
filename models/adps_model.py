from peewee import *

database = MySQLDatabase('supply_financial_reconciliation', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '10.0.0.127', 'port': 3306, 'user': 'erp', 'password': 'sd)*(YSHDG;l)D_FKds:D#&y}'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class BaseFeeItem(BaseModel):
    amount_conf = CharField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    fee_item_category = CharField()
    fee_item_code = CharField()
    fee_item_name = CharField()
    fee_item_name_en = CharField()
    fee_item_type = IntegerField()
    id = BigAutoField()
    remark = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'base_fee_item'
        indexes = (
            (('fee_item_code', 'del_flag'), True),
        )

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

class ReAnalysisRule(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    payment_channel_code = CharField(index=True)
    remark = CharField(null=True)
    rule_name = CharField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 're_analysis_rule'

class ReAnalysisRuleDetail(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    field_code = CharField(index=True, null=True)
    field_name = CharField(null=True)
    field_type = IntegerField(index=True, null=True)
    id = BigAutoField()
    mapping_group = UnknownField(null=True)  # json
    mapping_type = IntegerField(null=True)
    mapping_value = UnknownField(null=True)  # json
    regular_value = CharField(null=True)
    rule_id = BigIntegerField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 're_analysis_rule_detail'

class ReAnalysisRuleField(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    field_category = IntegerField(index=True, null=True)
    field_name = CharField(index=True, null=True)
    format_value = IntegerField(null=True)
    id = BigAutoField()
    must_flag = IntegerField(null=True)
    rule_id = BigIntegerField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 're_analysis_rule_field'

class ReBill(BaseModel):
    bill_code = CharField(constraints=[SQL("DEFAULT ''")])
    bill_finish_time = DateTimeField(null=True)
    bill_period_end_time = DateTimeField(null=True)
    bill_period_start_time = DateTimeField(null=True)
    bill_rule = IntegerField(null=True)
    channel_account = CharField(constraints=[SQL("DEFAULT ''")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    payment_channel = CharField(constraints=[SQL("DEFAULT ''")])
    state = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 're_bill'

class ReBillDetail(BaseModel):
    bill_amount = DecimalField(null=True)
    bill_code = CharField(constraints=[SQL("DEFAULT ''")])
    bill_currency = CharField(null=True)
    bill_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    business_code = CharField(null=True)
    business_name = CharField(null=True)
    business_no = CharField(null=True)
    card_group_code = CharField(null=True)
    channel_account = CharField(constraints=[SQL("DEFAULT ''")])
    confirm_time = DateTimeField(null=True)
    confirm_user_id = BigIntegerField(null=True)
    confirm_username = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    customer_card = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    difference_amount_type = IntegerField(null=True)
    difference_reason_remark = CharField(null=True)
    difference_reason_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    difference_type = IntegerField(null=True)
    external_transaction_id = CharField(null=True)
    fee_association_flag = IntegerField(null=True)
    fee_association_id = CharField(null=True)
    fee_association_parent_id = BigIntegerField(null=True)
    fee_item_category = CharField(null=True)
    fee_item_code = CharField(null=True)
    fee_item_id = BigIntegerField(null=True)
    fee_item_reconciled_flag = IntegerField(null=True)
    hm_detail_id = BigIntegerField(null=True)
    hm_transaction_amount = DecimalField(null=True)
    hm_transaction_currency = CharField(null=True)
    id = BigAutoField()
    mark_time = DateTimeField(null=True)
    mark_user_id = BigIntegerField(null=True)
    mark_username = CharField(null=True)
    payment_channel = CharField(constraints=[SQL("DEFAULT ''")])
    payment_channel_amount = DecimalField(null=True)
    payment_channel_currency = CharField(null=True)
    payment_channel_detail_id = BigIntegerField(null=True)
    payment_channel_settlement_amount = DecimalField(null=True)
    payment_channel_settlement_currency = CharField(null=True)
    payment_code = CharField(null=True)
    payment_time = DateTimeField(null=True)
    receiving_country = CharField(null=True)
    sales_order_code = CharField(null=True)
    sales_site = CharField(null=True)
    settlement_time = DateTimeField(null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")])
    trading_time = DateTimeField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 're_bill_detail'
        indexes = (
            (('del_flag', 'bill_code', 'fee_item_category'), False),
            (('del_flag', 'fee_association_id', 'fee_item_category'), False),
        )

class ReHmBill(BaseModel):
    account_status = IntegerField(null=True)
    bill_source = IntegerField(null=True)
    business_code = CharField(null=True)
    business_name = CharField(null=True)
    business_no = CharField(null=True)
    card_group_code = CharField(null=True)
    card_type = CharField(null=True)
    channel_account = CharField(null=True)
    country_code = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    currency = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    external_transaction_id = CharField(null=True)
    fee_item_code = CharField(null=True)
    fee_item_name = CharField(null=True)
    id = BigAutoField()
    invalid_remark = TextField(null=True)
    invalid_time = DateTimeField(null=True)
    invalid_username = CharField(null=True)
    order_no = CharField(null=True)
    pay_amount = DecimalField(null=True)
    pay_at = DateTimeField(null=True)
    payment_channel = CharField()
    payment_code = CharField(null=True)
    refund_is_dispute = IntegerField(null=True)
    refund_no = CharField(null=True)
    refund_type = IntegerField(null=True)
    rel_entry_bill_no = CharField(null=True)
    site = CharField(null=True)
    tax_info = UnknownField(null=True)  # json
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 're_hm_bill'
        indexes = (
            (('del_flag', 'rel_entry_bill_no'), False),
        )

class ReHmBillTemp(BaseModel):
    account_status = IntegerField(null=True)
    bill_source = IntegerField(null=True)
    business_code = CharField(null=True)
    business_name = CharField(null=True)
    business_no = CharField(null=True)
    card_group_code = CharField(null=True)
    card_type = CharField(null=True)
    channel_account = CharField(null=True)
    country_code = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    currency = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    external_transaction_id = CharField(null=True)
    fee_item_code = CharField(null=True)
    fee_item_name = CharField(null=True)
    id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    invalid_remark = TextField(null=True)
    invalid_time = DateTimeField(null=True)
    invalid_username = CharField(null=True)
    order_no = CharField(null=True)
    pay_amount = DecimalField(null=True)
    pay_at = DateTimeField(null=True)
    payment_channel = CharField()
    payment_code = CharField(null=True)
    refund_is_dispute = IntegerField(null=True)
    refund_no = CharField(null=True)
    refund_type = IntegerField(null=True)
    rel_entry_bill_no = CharField(null=True)
    site = CharField(null=True)
    tax_info = UnknownField(null=True)  # json
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 're_hm_bill_temp'
        primary_key = False

class RePaymentChannelBill(BaseModel):
    bill_code = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    import_time = DateTimeField(null=True)
    import_user_id = BigIntegerField(null=True)
    import_username = CharField(null=True)
    legal_entity = CharField()
    payment_channel_code = CharField()
    remark = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 're_payment_channel_bill'
        indexes = (
            (('payment_channel_code', 'legal_entity'), False),
        )

class RePaymentChannelBillAttachment(BaseModel):
    analysis_rule = UnknownField(null=True)  # json
    attachment_name = CharField(null=True)
    attachment_url = CharField(null=True)
    bill_code = CharField(index=True)
    bill_id = BigIntegerField(index=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 're_payment_channel_bill_attachment'

class RePaymentChannelBillDetail(BaseModel):
    account = CharField(null=True)
    bill_code = CharField(index=True)
    bill_id = BigIntegerField(index=True)
    card_group_code = CharField(null=True)
    commission_relate_id = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    customer_card_type = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    field_type = IntegerField(null=True)
    id = BigAutoField()
    import_time = DateTimeField(null=True)
    import_user_id = BigIntegerField(null=True)
    import_username = CharField(null=True)
    item_code = CharField(null=True)
    item_name = CharField(null=True)
    payment_code = CharField(null=True)
    relate_bill_code = CharField(null=True)
    settle_amount = DecimalField(null=True)
    settle_currency = CharField(null=True)
    settle_time = DateTimeField(null=True)
    state = IntegerField(null=True)
    trade_amount = DecimalField(null=True)
    trade_currency = CharField(null=True)
    trade_out_id = CharField(null=True)
    trade_time = DateTimeField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 're_payment_channel_bill_detail'
        indexes = (
            (('del_flag', 'relate_bill_code'), False),
        )

