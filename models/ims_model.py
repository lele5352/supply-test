from peewee import *

from config import db_config

database = MySQLDatabase('supply_ims', **db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class BlockBook(BaseModel):
    block_book_id = CharField(index=True)
    bom_version = CharField(null=True)
    book_state = IntegerField()
    change_qty = IntegerField()
    change_type = IntegerField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    event_code = CharField(index=True)
    event_desc = CharField()
    from_block_qty = IntegerField()
    from_location_qty = IntegerField()
    from_storage_location_id = BigIntegerField(null=True)
    from_storage_location_state = IntegerField()
    goods_sku_code = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    operate_log_id = BigIntegerField()
    relation_table_id = BigIntegerField()
    relation_table_name = CharField()
    source_no = CharField(index=True)
    storage_location_id = BigIntegerField(null=True)
    system_code = CharField()
    target_warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    to_block_qty = IntegerField()
    to_location_qty = IntegerField()
    to_storage_location_id = BigIntegerField(null=True)
    to_storage_location_state = IntegerField()
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ware_sku_code = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'block_book'


class BomDetail(BaseModel):
    bom_qty = IntegerField()
    bom_version = CharField()
    goods_sku_code = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ware_sku_code = CharField(index=True)

    class Meta:
        table_name = 'bom_detail'
        indexes = (
            (('goods_sku_code', 'ware_sku_code'), True),
        )


class CentralInventory(BaseModel):
    block = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_code = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    remain = IntegerField(constraints=[SQL("DEFAULT 0")])
    stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'central_inventory'
        indexes = (
            (('goods_sku_code', 'warehouse_id'), True),
        )


class GoodsInventory(BaseModel):
    current_warehouse_id = BigIntegerField()
    goods_sku_code = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    remain = IntegerField(constraints=[SQL("DEFAULT 0")])
    stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    target_warehouse_id = BigIntegerField(null=True)
    trace_id = CharField(null=True)
    type = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'goods_inventory'
        indexes = (
            (('goods_sku_code', 'current_warehouse_id', 'target_warehouse_id', 'type'), True),
        )


class IdempotentResult(BaseModel):
    create_time = DateTimeField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    param = CharField()
    param_json = UnknownField()  # json
    result = UnknownField(null=True)  # json
    trace_id = CharField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    uri = CharField()
    version = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'idempotent_result'
        indexes = (
            (('param', 'uri'), True),
        )


class NoSuitCheckRecord(BaseModel):
    all_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    bom_qty = IntegerField()
    bom_version = CharField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    goods_sku_code = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    no_suit_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    no_suit_type = IntegerField()
    target_warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ware_sku_code = CharField(index=True)
    warehouse_id = BigIntegerField(index=True)

    class Meta:
        table_name = 'no_suit_check_record'


class NogoodWaresInventory(BaseModel):
    block = IntegerField(constraints=[SQL("DEFAULT 0")])
    bom_version = CharField(null=True)
    goods_sku_code = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    storage_location_id = BigIntegerField(null=True)
    storage_location_type = IntegerField(null=True)
    target_warehouse_id = BigIntegerField(null=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ware_sku_code = CharField()
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'nogood_wares_inventory'
        indexes = (
            (('ware_sku_code', 'warehouse_id', 'storage_location_id'), True),
        )


class OperateLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    function_type = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    operate_type = CharField()
    operator_id = BigIntegerField(null=True)
    source_no = CharField()
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'operate_log'


class StockBook(BaseModel):
    bom_version = CharField(null=True)
    book_state = IntegerField()
    change_qty = IntegerField()
    change_remain = IntegerField(null=True)
    change_type = IntegerField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    event_code = CharField(index=True, null=True)
    event_desc = CharField(null=True)
    from_block_qty = IntegerField(null=True)
    from_location_qty = IntegerField()
    from_remain_qty = IntegerField(null=True)
    from_storage_location_id = BigIntegerField(null=True)
    from_storage_location_state = IntegerField()
    goods_sku_code = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    operate_log_id = BigIntegerField()
    relation_table_id = BigIntegerField()
    relation_table_name = CharField()
    source_no = CharField(index=True)
    stock_book_id = CharField(index=True)
    storage_location_id = BigIntegerField(null=True)
    system_code = CharField()
    target_warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    to_block_qty = IntegerField(null=True)
    to_location_qty = IntegerField()
    to_remain_qty = IntegerField(null=True)
    to_storage_location_id = BigIntegerField(null=True)
    to_storage_location_state = IntegerField()
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ware_sku_code = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'stock_book'


class StockCheckRecord(BaseModel):
    change_qty = IntegerField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    current_warehouse_id = BigIntegerField()
    from_qty = IntegerField(null=True)
    goods_sku_code = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    stock_remain = IntegerField(constraints=[SQL("DEFAULT 0")])
    table_id = BigIntegerField(null=True)
    table_name = CharField(constraints=[SQL("DEFAULT 'goods_inventory'")])
    target_warehouse_id = BigIntegerField(null=True)
    to_qty = IntegerField(null=True)
    trace_id = CharField(null=True)
    type = IntegerField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'stock_check_record'


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


class WaresInventory(BaseModel):
    block = IntegerField(constraints=[SQL("DEFAULT 0")])
    bom_version = CharField(null=True)
    goods_sku_code = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    storage_location_id = BigIntegerField(null=True)
    storage_location_type = IntegerField(null=True)
    target_warehouse_id = BigIntegerField(null=True)
    trace_id = CharField(null=True)
    type = IntegerField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ware_sku_code = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'wares_inventory'
        indexes = (
            (('ware_sku_code', 'warehouse_id', 'storage_location_id', 'target_warehouse_id', 'type'), True),
        )
