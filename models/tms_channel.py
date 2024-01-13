from peewee import *
from config import tms_db_config

database = MySQLDatabase('supply_logistics_channel', **tms_db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class ChChannelProp(BaseModel):
    channel_code = CharField()
    channel_id = BigIntegerField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    prop_key = CharField()
    prop_val = TextField()
    type = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'ch_channel_prop'


class ChChargeConfig(BaseModel):
    channel_code = CharField()
    channel_id = BigIntegerField()
    condition_x = IntegerField()
    condition_y = IntegerField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_address_id = BigIntegerField(null=True)
    effective_time = DateTimeField(null=True)
    ext_info = TextField(null=True)
    id = BigAutoField()
    remark = CharField(null=True)
    service_code = CharField(null=True)
    state = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'ch_charge_config'


class ChChargeConfigDetail(BaseModel):
    charge_config_id = BigIntegerField()
    condition_x_value = CharField(null=True)
    condition_y_value = CharField(null=True)
    config_value = CharField(null=True)
    create_time = DateTimeField()
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    create_username = CharField(constraints=[SQL("DEFAULT '0'")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    fee_categories = CharField(null=True)
    fee_categories_name = CharField(null=True)
    id = BigAutoField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'ch_charge_config_detail'


class ChChargeTrayConfig(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    height = DecimalField(null=True)
    id = BigAutoField()
    length = DecimalField(null=True)
    service_code = CharField()
    service_id = BigIntegerField(null=True)
    state = IntegerField(null=True)
    tray_type = CharField(null=True)
    unit = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    weight = DecimalField()
    weight_unit = CharField(null=True)
    width = DecimalField()

    class Meta:
        table_name = 'ch_charge_tray_config'


class ChCostPriceConfig(BaseModel):
    channel_code = CharField()
    channel_id = BigIntegerField()
    config_info = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    effective_time = DateTimeField()
    id = BigAutoField()
    remark = CharField(null=True)
    service_code = CharField()
    state = IntegerField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'ch_cost_price_config'


class ChCostPriceConfigDetail(BaseModel):
    charge_effective_mode = IntegerField(null=True)
    charge_rule = TextField(null=True)
    condition_effective_mode = IntegerField(null=True)
    condition_idx = IntegerField(null=True)
    condition_rule = TextField(null=True)
    cost_price_id = BigIntegerField()
    create_time = DateTimeField()
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    create_username = CharField(constraints=[SQL("DEFAULT '0'")], null=True)
    currency = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    fee_categories = CharField()
    id = BigAutoField()
    sort = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'ch_cost_price_config_detail'


class ChCutoffOrderConfig(BaseModel):
    channel_code = CharField()
    channel_id = BigIntegerField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    currency = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_address_id = BigIntegerField()
    freight_threshold = DecimalField(null=True)
    id = BigAutoField()
    order_quota = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'ch_cutoff_order_config'


class ChDeliveryRulesConfig(BaseModel):
    address_type = IntegerField()
    arrive_flag = IntegerField()
    channel_code = CharField()
    channel_id = BigIntegerField()
    city = CharField(null=True)
    country_code = CharField(null=True)
    country_name = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    province = CharField(null=True)
    province_name = CharField(null=True)
    region_group_id = BigIntegerField(null=True)
    region_group_name = CharField(null=True)
    restrict_type = IntegerField(null=True)
    restrict_value = CharField(null=True)
    rule_type = IntegerField()
    rule_value = CharField(null=True)
    service_code = CharField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'ch_delivery_rules_config'


class ChExpressSpecConfig(BaseModel):
    channel_code = CharField()
    channel_id = BigIntegerField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    print_copies = IntegerField(null=True)
    print_direction = IntegerField()
    scale = CharField()
    service_code = CharField()
    type = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'ch_express_spec_config'


class ChZoneConfig(BaseModel):
    channel_code = CharField()
    channel_id = BigIntegerField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_address_id = CharField(null=True)
    id = BigAutoField()
    service_code = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    zone_name = CharField(null=True)

    class Meta:
        table_name = 'ch_zone_config'


class ChZoneConfigDetail(BaseModel):
    city = CharField(null=True)
    country_code = CharField()
    country_name = CharField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    create_username = CharField(constraints=[SQL("DEFAULT '0'")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    postal_code = TextField(null=True)
    postal_type = IntegerField(null=True)
    province_code = CharField(null=True)
    province_name = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    zone_id = BigIntegerField()
    zone_type = IntegerField()

    class Meta:
        table_name = 'ch_zone_config_detail'


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


class LogisticsChannel(BaseModel):
    additional_services = CharField(null=True)
    auto_order_flag = IntegerField(null=True)
    channel_code = CharField()
    channel_name = CharField()
    channel_type = IntegerField(constraints=[SQL("DEFAULT 10")], null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    currency = CharField(null=True)
    cutoff_order_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_country = CharField(null=True)
    id = BigAutoField()
    logistics_brand = CharField(null=True)
    logistics_service = CharField(null=True)
    max_timeliness_day = IntegerField(null=True)
    min_timeliness_day = IntegerField(null=True)
    receipt_country = CharField(null=True)
    service_code = CharField(null=True)
    service_id = BigIntegerField(null=True)
    state = IntegerField(null=True)
    timeliness_level = IntegerField(null=True)
    transport_step = IntegerField()
    transport_type = IntegerField(null=True)
    trial_calc_info = CharField(null=True)
    unit = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'logistics_channel'


class LogisticsExternalInterfaceLog(BaseModel):
    create_time = DateTimeField()
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    create_username = CharField(constraints=[SQL("DEFAULT '0'")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    idempotent = CharField(null=True)
    interface_flag = IntegerField()
    order_code = CharField(constraints=[SQL("DEFAULT ''")])
    remark = CharField(null=True)
    request_content = TextField()
    request_time = DateTimeField(null=True)
    response_content = TextField(null=True)
    response_flag = IntegerField(constraints=[SQL("DEFAULT 1")])
    response_time = DateTimeField(null=True)
    source_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    source_order_flag = IntegerField()
    system_flag = IntegerField()
    trace_id = CharField(constraints=[SQL("DEFAULT '0'")])
    transaction_commit_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'logistics_external_interface_log'


class LogisticsService(BaseModel):
    cancel_order_type = IntegerField()
    contact_email = CharField(null=True)
    contact_name = CharField(null=True)
    contact_tel = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    invoice_info = CharField(null=True)
    place_order_type = IntegerField()
    service_code = CharField()
    service_name = CharField()
    state = IntegerField(constraints=[SQL("DEFAULT 0")])
    tracking_type = IntegerField(null=True)
    trial_calc_type = IntegerField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'logistics_service'


class LogisticsServiceAccount(BaseModel):
    access_token_validity = IntegerField(null=True)
    app_id = CharField(null=True)
    app_secrect = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ext_info = CharField(null=True)
    id = BigAutoField()
    password = CharField(null=True)
    refresh_token = CharField(null=True)
    refresh_token_validity = IntegerField(null=True)
    service_code = CharField(null=True)
    token = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    url = CharField(null=True)
    username = CharField(null=True)

    class Meta:
        table_name = 'logistics_service_account'


class LogisticsServiceConfig(BaseModel):
    config_key = CharField(null=True)
    config_key_type = IntegerField(null=True)
    config_type = IntegerField()
    config_value = TextField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    service_code = CharField(index=True)
    service_id = BigIntegerField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'logistics_service_config'


class LogisticsServiceOrderLog(BaseModel):
    barcode = CharField(null=True)
    channel_code = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(null=True)
    ext_data = TextField(null=True)
    file_url = CharField(null=True)
    id = BigAutoField()
    idempotent = CharField(null=True)
    order_code = CharField(null=True)
    service_code = CharField()
    source_file_url = CharField(null=True)
    source_order_code = CharField(null=True)
    state = IntegerField(null=True)
    track_order_code = CharField(null=True)
    transition_mark = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'logistics_service_order_log'


class LogisticsServiceOrderMapping(BaseModel):
    barcode = CharField(null=True)
    channel_code = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(null=True)
    ext_data = CharField(null=True)
    file_url = TextField(null=True)
    id = BigAutoField()
    idempotent = CharField(null=True)
    order_code = CharField(null=True)
    proof_url = TextField(null=True)
    service_code = CharField()
    source_file_url = TextField(null=True)
    source_order_code = CharField(null=True)
    source_proof_url = TextField(null=True)
    state = IntegerField(null=True)
    track_order_code = CharField(null=True)
    transition_mark = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'logistics_service_order_mapping'
        indexes = (
            (('service_code', 'channel_code', 'idempotent', 'del_flag'), False),
        )


class LogisticsServiceOrderMappingLog(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(null=True)
    host_name = CharField(null=True)
    id = BigAutoField()
    order_code = CharField(null=True)
    order_mapping_id = BigIntegerField(null=True)
    req_json = TextField(null=True)
    res_json = TextField(null=True)
    success_flag = IntegerField(null=True)
    third_order_code = CharField(null=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'logistics_service_order_mapping_log'


class LogisticsServiceParamConf(BaseModel):
    conf_name = CharField()
    conf_type = IntegerField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    order_conf = CharField(null=True)
    remark = CharField(null=True)
    required_flag = IntegerField()
    service_code = CharField()
    service_id = BigIntegerField(null=True)
    service_req_type = IntegerField(null=True)
    trial_calc_conf = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    val_range = TextField(null=True)

    class Meta:
        table_name = 'logistics_service_param_conf'


class LogisticsServiceRequestLog(BaseModel):
    channel_id = BigIntegerField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    log_type = IntegerField(constraints=[SQL("DEFAULT 10")])
    order_code = CharField()
    remark = CharField(null=True)
    req_url = CharField(null=True)
    resp_url = CharField(null=True)
    service_code = CharField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'logistics_service_request_log'
