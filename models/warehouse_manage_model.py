from peewee import *

database = MySQLDatabase('supply_warehouse_manage', **{'charset': 'utf8', 'sql_mode': 'PIPES_AS_CONCAT', 'use_unicode': True, 'host': '10.0.0.127', 'port': 3306, 'user': 'erp', 'password': 'sd)*(YSHDG;l)D_FKds:D#&y}'})

class UnknownField(object):
    def __init__(self, *_, **__): pass

class BaseModel(Model):
    class Meta:
        database = database

class AdjustReceipt(BaseModel):
    adjust_reason = IntegerField(null=True)
    adjust_receipt_code = CharField(unique=True)
    audit_time = DateTimeField(null=True)
    audit_user = BigIntegerField(null=True)
    audit_user_name = CharField(null=True)
    block_book_id = CharField(null=True)
    change_count = BigIntegerField()
    change_type = IntegerField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField(null=True)
    create_user_name = CharField(null=True)
    deal_status = IntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_code = CharField(index=True)
    id = BigAutoField()
    quality_status = IntegerField(null=True)
    reject_reason = CharField(null=True)
    relation_no = CharField(null=True)
    remark = CharField(null=True)
    source_type = IntegerField()
    status = IntegerField()
    storage_location_id = BigIntegerField()
    target_warehouse_id = BigIntegerField(null=True)
    warehouse_id = BigIntegerField()
    wares_sku_code = CharField(index=True)

    class Meta:
        table_name = 'adjust_receipt'

class FrozenReceipt(BaseModel):
    block_book_id = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField(null=True)
    create_user_name = CharField(null=True)
    deal_status = IntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    frozen_count = BigIntegerField()
    frozen_reason = IntegerField(null=True)
    frozen_receipt_code = CharField(unique=True)
    goods_sku_code = CharField(index=True)
    id = BigAutoField()
    remark = CharField(null=True)
    status = IntegerField()
    storage_location_id = CharField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    warehouse_id = BigIntegerField()
    wares_sku_code = CharField(index=True)

    class Meta:
        table_name = 'frozen_receipt'

class InventoryDelivery(BaseModel):
    category = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    deliver_time = DateTimeField(null=True)
    id = BigAutoField()
    sku_code = CharField(null=True)
    sku_qty = IntegerField(null=True)
    type = IntegerField(constraints=[SQL("DEFAULT 10")], null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'inventory_delivery'

class InventoryEntryBatch(BaseModel):
    batch_time = DateTimeField(null=True)
    category = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    sku_code = CharField(null=True)
    sku_qty = IntegerField(null=True)
    type = IntegerField(constraints=[SQL("DEFAULT 10")], null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'inventory_entry_batch'

class InventoryLifecycle(BaseModel):
    available_qty = IntegerField(null=True)
    current_order_category = IntegerField(null=True)
    current_order_id = BigIntegerField(null=True)
    current_order_no = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    inventory_type = IntegerField(null=True)
    parent_order_id = BigIntegerField(null=True)
    parent_order_no = CharField(null=True)
    sale_sku_code = CharField(null=True)
    sale_sku_component_qty = IntegerField(null=True)
    sku_code = CharField(index=True, null=True)
    sku_qty = IntegerField(null=True)
    source_order_create_time = DateTimeField(null=True)
    source_order_id = IntegerField(null=True)
    source_order_no = CharField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'inventory_lifecycle'

class InventoryLifecycleErrorLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    err_msg = CharField(null=True)
    id = BigAutoField()
    order_category = CharField(null=True)
    order_code = CharField(null=True)
    sku_code = CharField(null=True)
    sku_qty = IntegerField(null=True)
    type = IntegerField(constraints=[SQL("DEFAULT 10")], null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'inventory_lifecycle_error_log'

class InventoryLifecycleSimple(BaseModel):
    available_qty = IntegerField(null=True)
    batch_time = DateTimeField(null=True)
    category = CharField(null=True)
    cost_percent = DecimalField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    exhaust_time = DateTimeField(null=True)
    id = BigAutoField()
    sale_sku_code = CharField(null=True)
    sale_sku_component_qty = IntegerField(null=True)
    sku_code = CharField(null=True)
    sku_qty = IntegerField(null=True)
    type = IntegerField(constraints=[SQL("DEFAULT 10")], null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)
    warehouse_product_num = IntegerField(null=True)

    class Meta:
        table_name = 'inventory_lifecycle_simple'

class InventoryLifecycleSyncLog(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    sync_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'inventory_lifecycle_sync_log'

class ProcessReceipt(BaseModel):
    audit_time = DateTimeField(null=True)
    audit_user = BigIntegerField(null=True)
    audit_user_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField(null=True)
    create_user_name = CharField(null=True)
    deal_status = IntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    process_desc = CharField()
    process_receipt_code = CharField(unique=True)
    process_type = IntegerField()
    reject_reason = CharField(null=True)
    status = IntegerField()

    class Meta:
        table_name = 'process_receipt'

class ProcessReceiptBatchDetail(BaseModel):
    batch_no = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    process_receipt_detail_id = BigIntegerField()
    process_receipt_id = BigIntegerField()
    sku_code = CharField()
    sku_name = CharField(null=True)
    sku_qty = IntegerField()

    class Meta:
        table_name = 'process_receipt_batch_detail'

class ProcessReceiptDetail(BaseModel):
    batch_no = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_code = CharField()
    id = BigAutoField()
    process_count = BigIntegerField()
    process_receipt_id = BigIntegerField(index=True)
    proportion = IntegerField(null=True)
    quality_status = IntegerField()
    storage_location_id = CharField()
    storage_location_type = IntegerField()
    target_warehouse_id = BigIntegerField(null=True)
    type = IntegerField()
    warehouse_id = BigIntegerField()
    wares_sku_code = CharField(index=True)

    class Meta:
        table_name = 'process_receipt_detail'

class StockOperationBatchDetail(BaseModel):
    batch_no = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    sku_code = CharField(null=True)
    sku_name = CharField(null=True)
    sku_qty = IntegerField(null=True)
    stock_operation_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'stock_operation_batch_detail'

class StockOperationLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField(null=True)
    create_user_name = CharField(null=True)
    des_location_id = BigIntegerField()
    id = BigAutoField()
    operation_type = IntegerField()
    origin_location_id = BigIntegerField()
    request = UnknownField(null=True)  # json
    response = UnknownField(null=True)  # json
    serial_no = CharField(unique=True)
    status = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'stock_operation_log'
        indexes = (
            (('operation_type', 'status'), False),
        )

class TsoLocationBatch(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    location_code = CharField(index=True)
    location_id = BigIntegerField(index=True)
    source_code = CharField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'tso_location_batch'

class TsoLocationBatchDetail(BaseModel):
    batch_no = CharField(index=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    location_batch_id = BigIntegerField(index=True)
    sku_code = CharField(index=True)
    sku_qty = IntegerField()
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'tso_location_batch_detail'

class TsoSeataTemp(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()

    class Meta:
        table_name = 'tso_seata_temp'

class TsoStocktakingOrder(BaseModel):
    abnormal_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    first_accuracy = CharField(constraints=[SQL("DEFAULT ''")])
    id = BigAutoField()
    second_accuracy = CharField(constraints=[SQL("DEFAULT ''")])
    show_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_order_code = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    stocktaking_order_dimension = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_order_scope = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_order_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_order_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tso_stocktaking_order'

class TsoStocktakingOrderDetail(BaseModel):
    bom_version = CharField(constraints=[SQL("DEFAULT ''")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    sale_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sale_sku_name = CharField(constraints=[SQL("DEFAULT ''")])
    sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sku_name = CharField(constraints=[SQL("DEFAULT ''")])
    stocktaking_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    stocktaking_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    stocktaking_order_location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tso_stocktaking_order_detail'

class TsoStocktakingOrderLocation(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    location_code = CharField(constraints=[SQL("DEFAULT ''")])
    location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    location_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    location_state_remark = CharField(constraints=[SQL("DEFAULT ''")])
    pick_route = BigIntegerField(null=True)
    stocktaking_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    stocktaking_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_area_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_area_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tso_stocktaking_order_location'

class TsoStocktakingOrderOperateLog(BaseModel):
    content = TextField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    id = BigAutoField()
    operate_type = IntegerField()
    remark = CharField(null=True)
    result_content = TextField(null=True)
    stocktaking_order_id = BigIntegerField(null=True)
    trace_id = CharField(null=True)

    class Meta:
        table_name = 'tso_stocktaking_order_operate_log'

class TsoStocktakingOrderResult(BaseModel):
    bom_version = CharField(constraints=[SQL("DEFAULT ''")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    sale_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sale_sku_name = CharField(constraints=[SQL("DEFAULT ''")])
    sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sku_name = CharField(constraints=[SQL("DEFAULT ''")])
    stocktaking_num = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    stocktaking_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_order_location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_result = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_result_num = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tso_stocktaking_order_result'

class TsoStocktakingResult(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    operate_time = DateTimeField(null=True)
    operate_user_id = BigIntegerField(null=True)
    operate_username = CharField(null=True)
    remarks = CharField(null=True)
    source_order_code = CharField(null=True)
    state = IntegerField()
    stocktaking_num = IntegerField(null=True)
    stocktaking_order_code = CharField(index=True)
    stocktaking_order_id = BigIntegerField()
    stocktaking_order_type = IntegerField(null=True)
    stocktaking_result_code = CharField(index=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'tso_stocktaking_result'

class TsoStocktakingResultDetail(BaseModel):
    aft_stock_qty = IntegerField(null=True)
    audit_remarks = CharField(null=True)
    audit_state = IntegerField(null=True)
    audit_time = DateTimeField(null=True)
    audit_user_id = BigIntegerField(null=True)
    audit_username = CharField(null=True)
    block_id = CharField(null=True)
    bom_version = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    diffe_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    freeze_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    inventory_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    inventory_result = IntegerField(constraints=[SQL("DEFAULT 0")])
    operate_time = DateTimeField(null=True)
    operate_user_id = BigIntegerField(null=True)
    operate_username = CharField(null=True)
    pre_stock_qty = IntegerField(null=True)
    remarks = CharField(null=True)
    sale_sku_code = CharField(null=True)
    sale_sku_img = CharField(null=True)
    sale_sku_name = CharField(null=True)
    sku_code = CharField(index=True)
    sku_name = CharField(null=True)
    stock_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    stocktaking_count = IntegerField(null=True)
    stocktaking_order_code = CharField()
    stocktaking_order_id = BigIntegerField()
    stocktaking_result_code = CharField(index=True)
    stocktaking_result_id = BigIntegerField()
    stocktaking_task_code = CharField()
    stocktaking_task_id = BigIntegerField()
    target_freeze_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    warehouse_area_code = CharField()
    warehouse_id = BigIntegerField()
    warehouse_location_code = CharField()
    warehouse_location_id = BigIntegerField()

    class Meta:
        table_name = 'tso_stocktaking_result_detail'

class TsoStocktakingResultDetailBatch(BaseModel):
    aft_stock_qty = IntegerField(null=True)
    audit_remarks = CharField(null=True)
    audit_state = IntegerField(null=True)
    audit_time = DateTimeField(null=True)
    audit_user_id = BigIntegerField(null=True)
    audit_username = CharField(null=True)
    batch_num = CharField(null=True)
    bom_version = CharField()
    id = BigAutoField()
    inventory_num = IntegerField(null=True)
    inventory_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    inventory_result_code = CharField()
    inventory_result_id = BigIntegerField()
    operate_time = DateTimeField(null=True)
    operate_user_id = BigIntegerField(null=True)
    operate_username = CharField(null=True)
    pre_stock_qty = IntegerField(null=True)
    sale_sku_code = CharField(null=True)
    sale_sku_name = CharField(null=True)
    sku_code = CharField()
    sku_name = CharField(null=True)
    warehouse_area_code = CharField()
    warehouse_id = BigIntegerField()
    warehouse_location_code = CharField()

    class Meta:
        table_name = 'tso_stocktaking_result_detail_batch'

class TsoStocktakingTask(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    print_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    print_num = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    stocktaking_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_task_assignee_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_task_assignee_name = CharField(constraints=[SQL("DEFAULT ''")])
    stocktaking_task_assignee_time = DateTimeField(null=True)
    stocktaking_task_code = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    stocktaking_task_dimension = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_task_end_time = DateTimeField(null=True)
    stocktaking_task_scope = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_task_start_time = DateTimeField(null=True)
    stocktaking_task_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_task_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_task_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_task_user_name = CharField(constraints=[SQL("DEFAULT ''")])
    stocktaking_task_work_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tso_stocktaking_task'
        indexes = (
            (('del_flag', 'stocktaking_order_id'), False),
            (('warehouse_id', 'stocktaking_order_code', 'stocktaking_task_code'), False),
        )

class TsoStocktakingTaskDetail(BaseModel):
    bom_version = CharField(constraints=[SQL("DEFAULT ''")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    indx = BigIntegerField(null=True)
    location_code = CharField(constraints=[SQL("DEFAULT ''")])
    location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    remark = CharField(constraints=[SQL("DEFAULT ''")])
    sale_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sale_sku_name = CharField(constraints=[SQL("DEFAULT ''")])
    sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sku_name = CharField(constraints=[SQL("DEFAULT ''")])
    stock_num_end = IntegerField(null=True)
    stock_num_start = IntegerField(null=True)
    stocktaking_location_end_time = DateTimeField(null=True)
    stocktaking_location_start_time = DateTimeField(null=True)
    stocktaking_num = IntegerField(null=True)
    stocktaking_result = IntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_result_num = IntegerField(null=True)
    stocktaking_task_code = CharField(constraints=[SQL("DEFAULT ''")])
    stocktaking_task_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    stocktaking_task_location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_area_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_area_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tso_stocktaking_task_detail'

class TsoStocktakingTaskLocation(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField(constraints=[SQL("DEFAULT ''")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    location_code = CharField(constraints=[SQL("DEFAULT ''")])
    location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    stocktaking_task_code = CharField(constraints=[SQL("DEFAULT ''")])
    stocktaking_task_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    update_username = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_area_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_area_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tso_stocktaking_task_location'

class TsoTurnQualityOrder(BaseModel):
    bom_version = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    create_username = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    from_location_code = CharField(constraints=[SQL("DEFAULT ''")])
    from_location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    sale_sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True, null=True)
    sale_sku_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sku_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    to_location_code = CharField(constraints=[SQL("DEFAULT ''")])
    to_location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    trun_qty = IntegerField()
    turn_order_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    turn_order_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    update_username = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    warehouse_abbr = CharField(null=True)
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tso_turn_quality_order'

class UndoLog(BaseModel):
    branch_id = BigIntegerField()
    context = CharField()
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
        primary_key = False

class WarehouseSkuHistory(BaseModel):
    bom_version = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    id = BigAutoField()
    location_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    relation_order_code = CharField(constraints=[SQL("DEFAULT ''")], index=True, null=True)
    relation_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    relation_order_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    remark = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    sale_sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True, null=True)
    sale_sku_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    shelves_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], index=True, null=True)
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True, null=True)
    sku_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sku_stock = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    warehouse_area_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    warehouse_area_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'warehouse_sku_history'

class WarehouseSkuRelation(BaseModel):
    bom_version = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    id = BigAutoField()
    location_code = CharField(constraints=[SQL("DEFAULT ''")])
    location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    relation_order_code = CharField(constraints=[SQL("DEFAULT ''")], index=True, null=True)
    relation_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    relation_order_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    sale_sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sale_sku_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    shelves_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], index=True, null=True)
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sku_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    sku_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    warehouse_area_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    warehouse_area_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'warehouse_sku_relation'

