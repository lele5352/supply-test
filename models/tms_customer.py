from peewee import *
from config import tms_db_config

database = MySQLDatabase('supply_logistics_customer', **tms_db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class Customer(BaseModel):
    address = CharField(null=True)
    contacts = CharField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    customer_account = CharField(null=True)
    customer_app_key = CharField(null=True)
    customer_flag = IntegerField()
    customer_manager_id = BigIntegerField()
    customer_manager_name = CharField()
    customer_name = CharField()
    customer_state = IntegerField()
    customer_type = IntegerField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    email = CharField(unique=True)
    id = BigAutoField()
    remark = CharField(null=True)
    settlement_period = IntegerField(null=True)
    taxid_number = CharField(null=True)
    telephone = CharField()
    update_time = DateTimeField(index=True, null=True)
    update_user_id = BigIntegerField(index=True, null=True)
    update_username = CharField(null=True)
    withholding_method = IntegerField(index=True, null=True)

    class Meta:
        table_name = 'customer'


class CustomerAddress(BaseModel):
    address_code = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    address_detail = CharField()
    address_form_code = CharField()
    address_form_name = CharField()
    address_name = CharField(index=True)
    address_type = IntegerField()
    city_code = CharField()
    city_name = CharField()
    company_name = CharField(null=True)
    contacts = CharField()
    country_code = CharField(index=True)
    country_name = CharField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    customer_id = BigIntegerField()
    deadline_hour = IntegerField(null=True)
    deadline_minutes = IntegerField(null=True)
    deadline_time = DateTimeField(null=True)
    default_address = IntegerField(constraints=[SQL("DEFAULT 1")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    email = CharField(null=True)
    id = BigAutoField()
    latitude = CharField(null=True)
    longitude = CharField(null=True)
    phone = CharField()
    pickup_end_time = DateTimeField(null=True)
    pickup_start_time = DateTimeField(null=True)
    post_code = CharField(index=True)
    remark = CharField(null=True)
    state_province_code = CharField()
    state_province_name = CharField()
    tel = CharField(null=True)
    time_zone = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'customer_address'


class CustomerContractAttachmentInfo(BaseModel):
    attachment_type = IntegerField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    customer_contract_id = BigIntegerField(index=True)
    customer_id = BigIntegerField(index=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    origin_name = CharField()
    remark = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    url = CharField()

    class Meta:
        table_name = 'customer_contract_attachment_info'


class CustomerContractInfo(BaseModel):
    contract_name = CharField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    customer_id = BigIntegerField(index=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    effective_end_time = DateTimeField(null=True)
    effective_start_time = DateTimeField(null=True)
    id = BigAutoField()
    remark = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'customer_contract_info'


class CustomerLogisticsProduct(BaseModel):
    channel_id = BigIntegerField(index=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    customer_id = BigIntegerField(index=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    discount_rule_id = BigIntegerField(index=True)
    id = BigAutoField()
    logistics_product_id = BigIntegerField(index=True)
    remark = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'customer_logistics_product'


class CustomerProductAddress(BaseModel):
    channel_id = BigIntegerField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    customer_address_id = BigIntegerField()
    customer_id = BigIntegerField()
    customer_product_id = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_account = CharField(null=True)
    delivery_account_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    logistics_service_id = BigIntegerField(null=True)
    remark = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'customer_product_address'
        indexes = (
            (('customer_id', 'customer_address_id', 'logistics_service_id'), False),
        )


class FileOperationRecord(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    customer_id = BigIntegerField(index=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    file_type = IntegerField(null=True)
    file_url = CharField(null=True)
    id = BigAutoField()
    operation_desc = CharField(null=True)
    operation_node = IntegerField(null=True)
    operation_result = IntegerField(null=True)
    operation_type = IntegerField(null=True)
    remark = CharField(null=True)
    task_id = CharField(null=True, unique=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'file_operation_record'


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


class OperationLog(BaseModel):
    content = CharField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    customer_id = BigIntegerField(index=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    node = IntegerField()
    remark = CharField(null=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'operation_log'
