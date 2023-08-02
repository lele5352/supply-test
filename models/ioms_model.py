from peewee import *
from config import scms_db_config

database = MySQLDatabase('supply_financial_ioms', **scms_db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class BatchJobExecution(BaseModel):
    create_time = DateTimeField(column_name='CREATE_TIME')
    end_time = DateTimeField(column_name='END_TIME', null=True)
    exit_code = CharField(column_name='EXIT_CODE', null=True)
    exit_message = CharField(column_name='EXIT_MESSAGE', null=True)
    job_configuration_location = CharField(column_name='JOB_CONFIGURATION_LOCATION', null=True)
    job_execution_id = BigAutoField(column_name='JOB_EXECUTION_ID')
    job_instance_id = BigIntegerField(column_name='JOB_INSTANCE_ID', index=True)
    last_updated = DateTimeField(column_name='LAST_UPDATED', null=True)
    start_time = DateTimeField(column_name='START_TIME', null=True)
    status = CharField(column_name='STATUS', null=True)
    version = BigIntegerField(column_name='VERSION', null=True)

    class Meta:
        table_name = 'batch_job_execution'


class BatchJobExecutionContext(BaseModel):
    job_execution_id = BigAutoField(column_name='JOB_EXECUTION_ID')
    serialized_context = TextField(column_name='SERIALIZED_CONTEXT', null=True)
    short_context = CharField(column_name='SHORT_CONTEXT')

    class Meta:
        table_name = 'batch_job_execution_context'


class BatchJobExecutionParams(BaseModel):
    date_val = DateTimeField(column_name='DATE_VAL', null=True)
    double_val = FloatField(column_name='DOUBLE_VAL', null=True)
    identifying = CharField(column_name='IDENTIFYING')
    job_execution_id = BigIntegerField(column_name='JOB_EXECUTION_ID', index=True)
    key_name = CharField(column_name='KEY_NAME')
    long_val = BigIntegerField(column_name='LONG_VAL', null=True)
    string_val = CharField(column_name='STRING_VAL', null=True)
    type_cd = CharField(column_name='TYPE_CD')

    class Meta:
        table_name = 'batch_job_execution_params'
        primary_key = False


class BatchJobExecutionSeq(BaseModel):
    id = BigIntegerField(column_name='ID')
    unique_key = CharField(column_name='UNIQUE_KEY', unique=True)

    class Meta:
        table_name = 'batch_job_execution_seq'
        primary_key = False


class BatchJobInstance(BaseModel):
    job_instance_id = BigAutoField(column_name='JOB_INSTANCE_ID')
    job_key = CharField(column_name='JOB_KEY')
    job_name = CharField(column_name='JOB_NAME')
    version = BigIntegerField(column_name='VERSION', null=True)

    class Meta:
        table_name = 'batch_job_instance'
        indexes = (
            (('job_name', 'job_key'), True),
        )


class BatchJobSeq(BaseModel):
    id = BigIntegerField(column_name='ID')
    unique_key = CharField(column_name='UNIQUE_KEY', unique=True)

    class Meta:
        table_name = 'batch_job_seq'
        primary_key = False


class BatchStepExecution(BaseModel):
    commit_count = BigIntegerField(column_name='COMMIT_COUNT', null=True)
    end_time = DateTimeField(column_name='END_TIME', null=True)
    exit_code = CharField(column_name='EXIT_CODE', null=True)
    exit_message = CharField(column_name='EXIT_MESSAGE', null=True)
    filter_count = BigIntegerField(column_name='FILTER_COUNT', null=True)
    job_execution_id = BigIntegerField(column_name='JOB_EXECUTION_ID', index=True)
    last_updated = DateTimeField(column_name='LAST_UPDATED', null=True)
    process_skip_count = BigIntegerField(column_name='PROCESS_SKIP_COUNT', null=True)
    read_count = BigIntegerField(column_name='READ_COUNT', null=True)
    read_skip_count = BigIntegerField(column_name='READ_SKIP_COUNT', null=True)
    rollback_count = BigIntegerField(column_name='ROLLBACK_COUNT', null=True)
    start_time = DateTimeField(column_name='START_TIME')
    status = CharField(column_name='STATUS', null=True)
    step_execution_id = BigAutoField(column_name='STEP_EXECUTION_ID')
    step_name = CharField(column_name='STEP_NAME')
    version = BigIntegerField(column_name='VERSION')
    write_count = BigIntegerField(column_name='WRITE_COUNT', null=True)
    write_skip_count = BigIntegerField(column_name='WRITE_SKIP_COUNT', null=True)

    class Meta:
        table_name = 'batch_step_execution'


class BatchStepExecutionContext(BaseModel):
    serialized_context = TextField(column_name='SERIALIZED_CONTEXT', null=True)
    short_context = CharField(column_name='SHORT_CONTEXT')
    step_execution_id = BigAutoField(column_name='STEP_EXECUTION_ID')

    class Meta:
        table_name = 'batch_step_execution_context'


class BatchStepExecutionSeq(BaseModel):
    id = BigIntegerField(column_name='ID')
    unique_key = CharField(column_name='UNIQUE_KEY', unique=True)

    class Meta:
        table_name = 'batch_step_execution_seq'
        primary_key = False


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


class IoInventoryBatch(BaseModel):
    balance_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    batch_no = CharField(constraints=[SQL("DEFAULT ''")])
    bom_count = IntegerField(null=True)
    bom_map = IntegerField(null=True)
    bom_percentage = DecimalField(null=True)
    bom_version = CharField(null=True)
    business_no = CharField(constraints=[SQL("DEFAULT ''")])
    business_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    component_flag = IntegerField(null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    entry_no = CharField(null=True)
    entry_time = DateTimeField(null=True)
    finish_time = DateTimeField(null=True)
    goods_type = IntegerField(null=True)
    id = BigAutoField()
    inventory_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    relation_order_code = CharField(null=True)
    sale_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sale_sku_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    short_warehouse_name = CharField(null=True)
    sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sku_name = CharField(null=True)
    source_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    trade_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    unit_price = DecimalField(null=True)
    update_time = DateTimeField(null=True)
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'io_inventory_batch'
        indexes = (
            (('del_flag', 'warehouse_id', 'entry_no', 'component_flag'), False),
            (('del_flag', 'warehouse_id', 'inventory_type'), False),
            (('del_flag', 'warehouse_id', 'inventory_type', 'business_no', 'batch_no'), False),
            (('warehouse_id', 'batch_no'), False),
        )


class IoInventoryBatchFlow(BaseModel):
    balance_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    batch_no = CharField(constraints=[SQL("DEFAULT ''")])
    bom_count = IntegerField(null=True)
    bom_map = IntegerField(null=True)
    bom_percentage = DecimalField(null=True)
    bom_version = CharField(null=True)
    business_no = CharField(constraints=[SQL("DEFAULT ''")])
    business_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    component_flag = IntegerField(null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    entry_no = CharField(null=True)
    entry_time = DateTimeField(null=True)
    finish_time = DateTimeField(null=True)
    flow_flag = IntegerField(constraints=[SQL("DEFAULT 10")])
    flow_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_type = IntegerField(null=True)
    id = BigAutoField()
    inventory_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    relation_order_code = CharField(null=True)
    sale_sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sale_sku_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    short_warehouse_name = CharField(null=True)
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sku_name = CharField(null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    source_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    unique_id = CharField(constraints=[SQL("DEFAULT ''")])
    unit_price = DecimalField(null=True)
    update_time = DateTimeField(null=True)
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'io_inventory_batch_flow'


class IoNotCompleteStockBusinessFlow(BaseModel):
    batch_number = CharField()
    bom_map = IntegerField(null=True)
    bom_percentage = DecimalField(null=True)
    bom_total = IntegerField(null=True)
    bom_version = CharField(null=True)
    business_no = CharField(null=True)
    business_time = DateTimeField(null=True)
    business_type = IntegerField(null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    finish_time = DateTimeField(null=True)
    first_entry_number = CharField(null=True)
    first_entry_time = DateTimeField(null=True)
    flow_type = IntegerField(null=True)
    id = BigAutoField()
    remain_qty = IntegerField(null=True)
    sale_sku_code = CharField(null=True)
    short_warehouse_name = CharField(null=True)
    sku_deal_qty = IntegerField(null=True)
    stock_type = IntegerField(null=True)
    total_price = DecimalField(null=True)
    unit_price = DecimalField(null=True)
    update_time = DateTimeField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_name = CharField(null=True)
    warehouse_sku_code = CharField(null=True)

    class Meta:
        table_name = 'io_not_complete_stock_business_flow'
        indexes = (
            (('flow_type', 'stock_type', 'warehouse_code'), False),
        )


class IoNotCompleteStockSnapshot(BaseModel):
    batch_number = CharField()
    bom_map = IntegerField(null=True)
    bom_percentage = DecimalField(null=True)
    bom_total = IntegerField(null=True)
    bom_version = CharField(null=True)
    business_time = DateTimeField(index=True, null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    first_entry_time = DateTimeField(null=True)
    id = BigAutoField()
    link_warehouse_sku_age = DecimalField(null=True)
    sale_sku_code = CharField(null=True)
    short_warehouse_name = CharField(null=True)
    single_warehouse_entry_time = DateTimeField(null=True)
    single_warehouse_sku_age = DecimalField(null=True)
    sku_qty = IntegerField(null=True)
    stock_type = IntegerField(null=True)
    total_price = DecimalField(null=True)
    unit_price = DecimalField(null=True)
    update_time = DateTimeField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_name = CharField(null=True)
    warehouse_sku = CharField(null=True)

    class Meta:
        table_name = 'io_not_complete_stock_snapshot'


class IoSaleSkuBusinessFlow(BaseModel):
    batch_number = TextField()
    bom_percentage = DecimalField(null=True)
    bom_total = IntegerField(null=True)
    bom_version = CharField(null=True)
    business_no = CharField(null=True)
    business_time = DateTimeField(null=True)
    business_type = IntegerField(null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    finish_time = DateTimeField(null=True)
    first_entry_time = DateTimeField(null=True)
    flow_type = IntegerField(null=True)
    id = BigAutoField()
    sale_sku_code = CharField(null=True)
    short_warehouse_name = CharField(null=True)
    sku_deal_qty = IntegerField(null=True)
    stock_type = IntegerField(null=True)
    total_price = DecimalField(null=True)
    update_time = DateTimeField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'io_sale_sku_business_flow'
        indexes = (
            (('flow_type', 'stock_type', 'warehouse_code'), False),
        )


class IoSaleSkuStockSnapshot(BaseModel):
    batch_number = TextField()
    belong_sale_sku = CharField(null=True)
    bom_map = IntegerField(null=True)
    bom_percentage = DecimalField(null=True)
    bom_total = IntegerField(null=True)
    bom_version = CharField(null=True)
    business_time = DateTimeField(index=True, null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    first_entry_time = DateTimeField(null=True)
    id = BigAutoField()
    link_warehouse_sku_age = DecimalField(null=True)
    short_warehouse_name = CharField(null=True)
    single_warehouse_entry_time = DateTimeField(null=True)
    single_warehouse_sku_age = DecimalField(null=True)
    sku_qty = IntegerField(null=True)
    stock_type = IntegerField(null=True)
    total_price = DecimalField(null=True)
    unit_price = DecimalField(null=True)
    update_time = DateTimeField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_name = CharField(null=True)

    class Meta:
        table_name = 'io_sale_sku_stock_snapshot'


class IoSourceOrder(BaseModel):
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    handle_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    operate_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    order_code = CharField()
    order_type = IntegerField()
    state = IntegerField()
    update_time = DateTimeField(null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'io_source_order'
        indexes = (
            (('order_type', 'order_code'), True),
        )


class IoSourceOrderDetail(BaseModel):
    bom_count = IntegerField(null=True)
    bom_scale = DecimalField(null=True)
    bom_version = CharField(null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    distribute_order_code = CharField(null=True)
    finish_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    flow_type = IntegerField(null=True)
    goods_type = IntegerField(null=True)
    id = BigAutoField()
    order_create_time = DateTimeField(null=True)
    order_type = IntegerField(null=True)
    purchase_price = DecimalField(null=True)
    sale_sku_code = CharField(null=True)
    sale_sku_name = CharField(null=True)
    sku_code = CharField(null=True)
    sku_name = CharField(null=True)
    sku_qty = IntegerField(null=True)
    source_order_code = CharField()
    source_order_id = BigIntegerField(null=True)
    unit_flag = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    warehouse_code = CharField()
    warehouse_id = BigIntegerField(null=True)
    warehouse_name = CharField(null=True)
    warehouse_short_name = CharField(null=True)

    class Meta:
        table_name = 'io_source_order_detail'
        indexes = (
            (('source_order_code', 'sale_sku_code', 'sku_code', 'unit_flag', 'flow_type'), True),
        )


class IoSourceOrderHandleDetail(BaseModel):
    bom_count = IntegerField(null=True)
    bom_scale = DecimalField(null=True)
    bom_version = CharField(null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    distribute_order_code = CharField(null=True)
    finish_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    flow_type = IntegerField(null=True)
    goods_type = IntegerField(null=True)
    handle_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    inventory_type = IntegerField(null=True)
    order_create_time = DateTimeField(null=True)
    order_type = IntegerField(null=True)
    purchase_price = DecimalField(null=True)
    relation_order_code = CharField(null=True)
    sale_sku_code = CharField(null=True)
    sale_sku_name = CharField(null=True)
    sku_code = CharField(null=True)
    sku_name = CharField(null=True)
    sku_qty = IntegerField(null=True)
    source_order_code = CharField()
    source_order_id = BigIntegerField()
    unit_flag = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    warehouse_code = CharField()
    warehouse_id = BigIntegerField(null=True)
    warehouse_name = CharField(null=True)
    warehouse_short_name = CharField(null=True)

    class Meta:
        table_name = 'io_source_order_handle_detail'
        indexes = (
            (('source_order_code', 'order_type', 'sale_sku_code', 'sku_code', 'inventory_type', 'flow_type',
              'distribute_order_code', 'unit_flag'), True),
        )


class IoWarehouseSkuBusinessFlow(BaseModel):
    batch_number = CharField()
    bom_map = IntegerField(null=True)
    bom_percentage = DecimalField(null=True)
    bom_total = IntegerField(null=True)
    bom_version = CharField(null=True)
    business_no = CharField(null=True)
    business_time = DateTimeField(null=True)
    business_type = IntegerField(null=True)
    component_flag = IntegerField(null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    finish_time = DateTimeField(null=True)
    first_entry_number = CharField(null=True)
    first_entry_time = DateTimeField(null=True)
    flow_type = IntegerField(null=True)
    goods_type = IntegerField(null=True)
    id = BigAutoField()
    remain_qty = IntegerField(null=True)
    sale_sku_code = CharField(null=True)
    short_warehouse_name = CharField(null=True)
    sku_deal_qty = IntegerField(null=True)
    stock_type = IntegerField(null=True)
    total_price = DecimalField(null=True)
    unit_price = DecimalField(null=True)
    update_time = DateTimeField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_name = CharField(null=True)
    warehouse_sku_code = CharField(null=True)

    class Meta:
        table_name = 'io_warehouse_sku_business_flow'


class IoWarehouseSkuStockSnapshot(BaseModel):
    batch_number = CharField()
    bom_map = IntegerField(null=True)
    bom_percentage = DecimalField(null=True)
    bom_total = IntegerField(null=True)
    bom_version = CharField(null=True)
    business_time = DateTimeField(index=True, null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    first_entry_time = DateTimeField(null=True)
    id = BigAutoField()
    link_warehouse_sku_age = DecimalField(null=True)
    sale_sku_code = CharField(null=True)
    short_warehouse_name = CharField(null=True)
    single_warehouse_entry_time = DateTimeField(null=True)
    single_warehouse_sku_age = DecimalField(null=True)
    sku_qty = IntegerField(null=True)
    stock_type = IntegerField(null=True)
    total_price = DecimalField(null=True)
    unit_price = DecimalField(null=True)
    update_time = DateTimeField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_name = CharField(null=True)
    warehouse_sku = CharField(null=True)

    class Meta:
        table_name = 'io_warehouse_sku_stock_snapshot'


class WaresInventory(BaseModel):
    block = IntegerField(constraints=[SQL("DEFAULT 0")])
    bom_version = CharField(null=True)
    goods_sku_code = CharField(index=True, null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    storage_location_id = BigIntegerField(null=True)
    storage_location_type = IntegerField(null=True)
    target_warehouse_id = BigIntegerField(index=True, null=True)
    trace_id = CharField(null=True)
    type = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ware_sku_code = CharField(index=True, null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'wares_inventory'
        indexes = (
            (('ware_sku_code', 'warehouse_id', 'storage_location_id', 'target_warehouse_id', 'type'), True),
        )
