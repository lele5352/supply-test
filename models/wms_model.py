from peewee import *

from config.sys_config import db_config

database = MySQLDatabase('supply_wms', **db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class BaseWarehouse(BaseModel):
    business_time = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    drawback_type = IntegerField(null=True)
    id = BigAutoField()
    locate_region = IntegerField(null=True)
    operate_mode = CharField(null=True)
    prop_info = TextField(null=True)
    short_warehouse_name = CharField(null=True)
    state = IntegerField(index=True, null=True)
    type = IntegerField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_code = CharField(null=True, unique=True)
    warehouse_name = CharField(null=True)
    warehouse_name_en = CharField(null=True)

    class Meta:
        table_name = 'base_warehouse'


class BaseWarehouseAddress(BaseModel):
    address = CharField(null=True)
    city_code = CharField(null=True)
    city_name = CharField(null=True)
    contact = CharField(null=True)
    country_code = CharField(null=True)
    country_name = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    district_code = CharField(null=True)
    district_name = CharField(null=True)
    email = CharField(null=True)
    id = BigAutoField()
    phone = CharField(null=True)
    postcode = CharField(null=True)
    province_code = CharField(null=True)
    province_name = CharField(null=True)
    street_code = CharField(null=True)
    street_name = CharField(null=True)
    tel = CharField(null=True)
    type = IntegerField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'base_warehouse_address'


class BaseWarehouseArea(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    state = IntegerField(null=True)
    type = IntegerField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_area_code = CharField(null=True)
    warehouse_area_name = CharField(null=True)
    warehouse_code = CharField(index=True, null=True)
    warehouse_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'base_warehouse_area'


class BaseWarehouseAreaCopy1(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    state = IntegerField(null=True)
    type = IntegerField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_area_code = CharField(null=True)
    warehouse_area_name = CharField(null=True)
    warehouse_code = CharField(index=True, null=True)
    warehouse_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'base_warehouse_area_copy1'


class BaseWarehouseAreaCopy2(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    state = IntegerField(null=True)
    type = IntegerField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_area_code = CharField(null=True)
    warehouse_area_name = CharField(null=True)
    warehouse_code = CharField(index=True, null=True)
    warehouse_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'base_warehouse_area_copy2'


class BaseWarehouseLocation(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    dest_warehouse_code = CharField(null=True)
    dest_warehouse_id = BigIntegerField(null=True)
    id = BigAutoField()
    pick_route = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    state = IntegerField(index=True, null=True)
    type = IntegerField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    use_state = IntegerField(index=True, null=True)
    warehouse_area_code = CharField(null=True)
    warehouse_area_id = BigIntegerField(index=True, null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(index=True, null=True)
    warehouse_location_code = CharField(null=True)
    warehouse_location_name = CharField(null=True)

    class Meta:
        table_name = 'base_warehouse_location'


class EnEntryOrder(BaseModel):
    create_time = DateTimeField(index=True, null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(null=True)
    dest_warehouse_code = CharField(null=True)
    dest_warehouse_id = BigIntegerField(null=True)
    distribute_order_code = CharField(null=True)
    entry_order_code = CharField(unique=True)
    first_arrival_time = DateTimeField(null=True)
    follow_up_uid = BigIntegerField(null=True)
    follow_up_username = CharField(null=True)
    id = BigAutoField()
    last_arrival_time = DateTimeField(null=True)
    plan_arrival_time = DateTimeField(null=True)
    purchase_order_code = CharField(null=True)
    quality_type = IntegerField()
    remarks = CharField(null=True)
    state = IntegerField(index=True, null=True)
    supplier_code = CharField(null=True)
    supplier_name = CharField(null=True)
    supplier_type = IntegerField(null=True)
    type = IntegerField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'en_entry_order'


class EnEntryOrderDetail(BaseModel):
    abnormal_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    actual_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    bom_version = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    defective_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    del_flag = IntegerField(index=True)
    entry_order_id = BigIntegerField(index=True)
    gp_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    height = DecimalField(null=True)
    id = BigAutoField()
    inspect_abnormal_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    length = DecimalField(null=True)
    plan_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    receipt_abnormal_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sale_sku_code = CharField()
    sale_sku_name = CharField()
    sale_sku_purchase_price = DecimalField(null=True)
    sale_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    shelves_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sku_code = CharField(index=True, null=True)
    sku_img = CharField(null=True)
    sku_name = CharField()
    sku_name_en = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_sku_name_suffix = CharField(null=True)
    weight = DecimalField(null=True)
    width = DecimalField(null=True)

    class Meta:
        table_name = 'en_entry_order_detail'


class EnEntryOrderDetailBatchRecord(BaseModel):
    actual_sku_qty = IntegerField()
    batch_number = CharField()
    create_time = DateTimeField()
    create_user = BigIntegerField()
    create_username = CharField()
    del_flag = IntegerField(null=True)
    entry_order_detail_id = BigIntegerField()
    entry_order_id = BigIntegerField()
    id = BigAutoField()
    plan_sku_qty = IntegerField()
    sku_code = CharField()
    update_time = DateTimeField(null=True)
    update_user = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'en_entry_order_detail_batch_record'


class EnEntryOrderLogistics(BaseModel):
    car_number = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(null=True)
    deliverer_name = CharField(null=True)
    entry_order_id = BigIntegerField(index=True, null=True)
    id = BigAutoField()
    logistics_company_code = CharField(null=True)
    logistics_company_name = CharField(null=True)
    phone = CharField(null=True)
    shipment_number = CharField(null=True)
    tel = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'en_entry_order_logistics'


class EnEntryOrderOperateLog(BaseModel):
    content = TextField()
    create_time = DateTimeField()
    create_user = BigIntegerField(null=True)
    create_username = CharField(null=True)
    entry_order_id = BigIntegerField(null=True)
    id = BigAutoField()
    operate_type = IntegerField()
    remark = CharField(null=True)
    result_content = TextField(null=True)
    trace_id = CharField(null=True)

    class Meta:
        table_name = 'en_entry_order_operate_log'


class EnExceptionOrder(BaseModel):
    cancel_remark = CharField(null=True)
    cancel_time = DateTimeField(null=True)
    commit_time = DateTimeField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    distribute_order_code = CharField(null=True)
    entry_order_code = CharField(null=True)
    entry_order_id = BigIntegerField(null=True)
    exception_order_code = CharField(null=True)
    handle_time = DateTimeField(null=True)
    id = BigAutoField()
    state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'en_exception_order'


class EnExceptionOrderDetail(BaseModel):
    cancel_remark = CharField(null=True)
    cancel_time = DateTimeField(null=True)
    cancel_user_id = BigIntegerField(null=True)
    cancel_username = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    description = CharField(null=True)
    entry_order_detail_id = BigIntegerField(null=True)
    exception_detail_code = CharField(null=True)
    exception_order_id = BigIntegerField(null=True)
    handled_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    qty = IntegerField(null=True)
    rel_order_codes = CharField(null=True)
    sale_sku_code = CharField(null=True)
    sku_code = CharField(null=True)
    sku_name = CharField(null=True)
    source = IntegerField(null=True)
    state = IntegerField(null=True)
    type = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'en_exception_order_detail'


class EnExceptionOrderDetailLocation(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    exception_order_detail_id = BigIntegerField(null=True)
    id = BigAutoField()
    location_code = CharField(null=True)
    location_id = BigIntegerField(null=True)
    qty = IntegerField(null=True)

    class Meta:
        table_name = 'en_exception_order_detail_location'


class EnExceptionOrderDetailPic(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    exception_order_detail_id = BigIntegerField(null=True)
    id = BigAutoField()
    url = CharField(null=True)

    class Meta:
        table_name = 'en_exception_order_detail_pic'


class EnExceptionOrderDetailSolution(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    exception_order_detail_id = BigIntegerField(null=True)
    handle_remark = CharField(null=True)
    handle_time = DateTimeField(null=True)
    handle_user_id = BigIntegerField(null=True)
    handle_username = CharField(null=True)
    id = BigAutoField()
    pur_remark = CharField(null=True)
    qty = IntegerField(null=True)
    solution_code = CharField(null=True)
    state = IntegerField(null=True)
    type = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'en_exception_order_detail_solution'


class EnPredictReceiptOrder(BaseModel):
    create_time = DateTimeField(index=True, null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    entry_order_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    entry_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    id = BigAutoField()
    predict_receipt_order_code = CharField(unique=True)
    receipt_order_code = CharField(index=True, null=True)
    receipt_order_id = BigIntegerField(index=True, null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'en_predict_receipt_order'


class EnPredictReceiptOrderDetail(BaseModel):
    bom_version = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(index=True, null=True)
    height = DecimalField(null=True)
    id = BigAutoField()
    length = DecimalField(null=True)
    location_code = CharField(constraints=[SQL("DEFAULT ''")])
    location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    predict_receipt_order_code = CharField()
    predict_receipt_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    sale_sku_code = CharField(constraints=[SQL("DEFAULT '0'")])
    sale_sku_name = CharField()
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sku_img = CharField(null=True)
    sku_name = CharField(null=True)
    sku_name_en = CharField(null=True)
    sku_qty = IntegerField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_area_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_area_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    weight = DecimalField(null=True)
    width = DecimalField(null=True)

    class Meta:
        table_name = 'en_predict_receipt_order_detail'


class EnQualityOrder(BaseModel):
    create_time = DateTimeField(index=True, null=True)
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    entry_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    entry_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    id = BigAutoField()
    quality_order_code = CharField(constraints=[SQL("DEFAULT ''")], unique=True)
    quality_time = DateTimeField(null=True)
    quality_user = BigIntegerField(null=True)
    quality_username = CharField(null=True)
    receipt_order_id = BigIntegerField(index=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    transfer_time = DateTimeField(null=True)
    transfer_user = BigIntegerField(null=True)
    transfer_username = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'en_quality_order'


class EnQualityOrderDetail(BaseModel):
    boom_version = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], index=True, null=True)
    entry_order_detail_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    height = DecimalField(null=True)
    id = BigAutoField()
    length = DecimalField(null=True)
    location_code = CharField(constraints=[SQL("DEFAULT ''")])
    location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    quality_order_id = BigIntegerField(index=True)
    quality_remark = CharField(null=True)
    quality_result = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    receipt_order_id = BigIntegerField(index=True)
    sale_sku_code = CharField(constraints=[SQL("DEFAULT '0'")])
    sale_sku_name = CharField(null=True)
    sku_code = CharField()
    sku_img = CharField(null=True)
    sku_name = CharField(null=True)
    sku_name_en = CharField(null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    warehouse_area_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_code = CharField()
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    weight = DecimalField(null=True)
    width = DecimalField(null=True)

    class Meta:
        table_name = 'en_quality_order_detail'


class EnQualityResultPic(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    img_url = CharField(null=True)
    quality_order_detail_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    quality_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    receipt_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    sku_code = CharField(null=True)

    class Meta:
        table_name = 'en_quality_result_pic'


class EnReceiptOrder(BaseModel):
    create_time = DateTimeField(index=True, null=True)
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    entry_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    entry_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    id = BigAutoField()
    quality_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    receipt_order_code = CharField(constraints=[SQL("DEFAULT '0'")], unique=True)
    receipt_time = DateTimeField(null=True)
    receipt_user = BigIntegerField(null=True)
    receipt_username = CharField(null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    transfer_time = DateTimeField(null=True)
    transfer_user = BigIntegerField(null=True)
    transfer_username = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'en_receipt_order'


class EnReceiptOrderDetail(BaseModel):
    bom_version = CharField(null=True)
    del_flag = IntegerField(index=True, null=True)
    height = DecimalField(null=True)
    id = BigAutoField()
    length = DecimalField(null=True)
    location_code = CharField(constraints=[SQL("DEFAULT ''")])
    location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    receipt_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    sale_sku_code = CharField(constraints=[SQL("DEFAULT '0'")])
    sale_sku_name = CharField()
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sku_img = CharField(null=True)
    sku_name = CharField(null=True)
    sku_name_en = CharField(null=True)
    sku_qty = IntegerField()
    warehouse_area_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_area_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")])
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    weight = DecimalField(null=True)
    width = DecimalField(null=True)

    class Meta:
        table_name = 'en_receipt_order_detail'


class EnReceiptOrderDetailBatchRecord(BaseModel):
    batch_number = CharField()
    create_time = DateTimeField()
    create_user = BigIntegerField()
    create_username = CharField()
    del_flag = IntegerField(null=True)
    id = BigAutoField()
    receipt_order_detail_id = BigIntegerField()
    receipt_order_id = BigIntegerField()
    sku_code = CharField(null=True)
    sku_qty = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'en_receipt_order_detail_batch_record'


class EnShelvesOrder(BaseModel):
    create_time = DateTimeField(index=True)
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField()
    del_flag = IntegerField(index=True, null=True)
    entry_order_code = CharField()
    entry_order_id = BigIntegerField()
    id = BigAutoField()
    shelves_order_code = CharField(index=True)
    shelves_time = DateTimeField(null=True)
    shelves_user = BigIntegerField(null=True)
    shelves_username = CharField(null=True)
    source_order_code = CharField()
    source_order_id = BigIntegerField()
    source_order_type = IntegerField(index=True)
    state = IntegerField(index=True, null=True)
    sync_ims = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sync_scm = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'en_shelves_order'


class EnShelvesOrderDetail(BaseModel):
    abnormal_qty = IntegerField(null=True)
    create_time = DateTimeField()
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField()
    del_flag = IntegerField(index=True, null=True)
    id = BigAutoField()
    sale_sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    shelves_order_code = CharField()
    shelves_order_id = BigIntegerField(index=True)
    shelves_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sku_code = CharField(null=True)
    sku_qty = IntegerField(null=True)
    source_location_code = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_location_code = CharField()
    warehouse_location_id = BigIntegerField(index=True)

    class Meta:
        table_name = 'en_shelves_order_detail'


class EnShelvesOrderDetailBatchRecord(BaseModel):
    batch_number = CharField()
    create_time = DateTimeField()
    create_user_id = BigIntegerField()
    create_username = CharField()
    del_flag = IntegerField(null=True)
    id = BigAutoField()
    shelves_order_detail_id = BigIntegerField()
    shelves_order_id = BigIntegerField()
    sku_code = CharField(null=True)
    sku_qty = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'en_shelves_order_detail_batch_record'


class OtherStockOutOrder(BaseModel):
    block_book_id = CharField(null=True)
    create_time = DateTimeField(index=True, null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(null=True)
    deliver_time = DateTimeField(null=True)
    deliver_username = CharField(null=True)
    id = BigAutoField()
    other_stock_out_order = CharField(unique=True)
    product_state = IntegerField()
    remark = CharField(null=True)
    source_order_code = CharField(null=True)
    state = IntegerField()
    stock_book_id = CharField(null=True)
    supplier_code = CharField(null=True)
    supplier_name = CharField(null=True)
    type = IntegerField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField(index=True)

    class Meta:
        table_name = 'other_stock_out_order'


class OtherStockOutOrderFlow(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    other_stock_out_id = BigIntegerField(index=True)
    third_block_id = CharField(null=True)
    third_business_no = CharField(null=True)
    type = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)

    class Meta:
        table_name = 'other_stock_out_order_flow'


class OtherStockOutOrderLogistics(BaseModel):
    car_num = CharField(null=True)
    contact = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(null=True)
    id = BigAutoField()
    logistics_name = CharField(null=True)
    logistics_order = CharField(null=True)
    other_stock_out_id = BigIntegerField(index=True, null=True)
    phone = CharField(null=True)
    remark = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'other_stock_out_order_logistics'


class OtherStockOutOrderSku(BaseModel):
    bom_version = CharField()
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(null=True)
    id = BigAutoField()
    image = CharField(null=True)
    other_stock_out_id = BigIntegerField(index=True)
    sale_sku_code = CharField()
    sale_sku_name = CharField()
    sku_code = CharField(index=True)
    sku_name = CharField(null=True)
    stock_out_qty = IntegerField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'other_stock_out_order_sku'


class OtherStockOutOrderSkuLocation(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(null=True)
    id = BigAutoField()
    other_stock_out_id = BigIntegerField(index=True)
    other_stock_out_sku_id = BigIntegerField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_location_code = CharField()
    warehouse_location_id = BigIntegerField()
    warehouse_location_name = CharField()
    warehouse_location_qty = IntegerField()

    class Meta:
        table_name = 'other_stock_out_order_sku_location'


class TdoAbnormalOrder(BaseModel):
    abnormal_order_code = CharField(unique=True)
    abnormal_order_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    abnormal_order_type = IntegerField()
    create_time = DateTimeField(index=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    customer_flag = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_order_code = CharField(index=True)
    delivery_order_id = BigIntegerField(index=True)
    handler_time = DateTimeField(null=True)
    handler_user_id = BigIntegerField(null=True)
    handler_username = CharField(null=True)
    id = BigAutoField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'tdo_abnormal_order'


class TdoAbnormalOrderDetail(BaseModel):
    abnormal_order_id = BigIntegerField(index=True)
    abnormal_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    demand_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    express_order_id = BigIntegerField(null=True)
    id = BigAutoField()
    pick_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    review_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sale_sku_code = CharField()
    sale_sku_img = CharField(null=True)
    sale_sku_name = CharField()
    sku_code = CharField()
    sku_name = CharField()

    class Meta:
        table_name = 'tdo_abnormal_order_detail'


class TdoAbnormalOrderSkuDetail(BaseModel):
    abnormal_order_detail_id = BigIntegerField(index=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    location_code = CharField(null=True)
    location_id = BigIntegerField(null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    warehouse_area_code = CharField(null=True)
    warehouse_area_id = BigIntegerField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'tdo_abnormal_order_sku_detail'


class TdoDeliveryOrder(BaseModel):
    block_book_id = CharField(null=True)
    cancel_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    check_time = DateTimeField(null=True)
    create_time = DateTimeField(index=True)
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


class TdoDeliveryOrderOperateLog(BaseModel):
    content = TextField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    delivery_order_id = BigIntegerField(null=True)
    id = BigAutoField()
    operate_type = IntegerField()
    remark = CharField(null=True)
    result_content = TextField(null=True)
    trace_id = CharField(null=True)

    class Meta:
        table_name = 'tdo_delivery_order_operate_log'


class TdoDeliveryOrderProp(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_order_code = CharField(null=True)
    delivery_order_id = BigIntegerField(null=True)
    id = BigAutoField()
    prop_key = IntegerField(null=True)
    prop_value = CharField(null=True)

    class Meta:
        table_name = 'tdo_delivery_order_prop'


class TdoDeliveryPackage(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_order_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    delivery_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    express_change_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    express_change_version = CharField(null=True)
    express_order_id = BigIntegerField(null=True)
    express_order_state = IntegerField()
    handover_time = DateTimeField(null=True)
    height = DecimalField(null=True)
    id = BigAutoField()
    length = DecimalField(null=True)
    pack_ext_info = CharField(null=True)
    package_code = CharField(null=True, unique=True)
    recheck_time = DateTimeField(null=True)
    recheck_user_id = BigIntegerField(null=True)
    recheck_username = CharField(null=True)
    remarks = CharField(null=True)
    state = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    weight = DecimalField(null=True)
    width = DecimalField(null=True)

    class Meta:
        table_name = 'tdo_delivery_package'


class TdoDeliveryPackageDetail(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    package_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    sale_sku_code = CharField(null=True)
    sale_sku_name = CharField(null=True)
    sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sku_id = IntegerField()
    sku_name = CharField(null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tdo_delivery_package_detail'


class TdoDeliveryPickDetail(BaseModel):
    channel_code = CharField(null=True)
    channel_name = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_order_code = CharField(index=True, null=True)
    delivery_order_id = BigIntegerField(index=True)
    delivery_stock_detail_id = BigIntegerField(null=True)
    id = BigAutoField()
    location_code = CharField(constraints=[SQL("DEFAULT ''")])
    location_id = BigIntegerField()
    logistics_code = CharField(null=True)
    logistics_name = CharField(null=True)
    package_code = CharField()
    pick_order_detail_id = BigIntegerField()
    pick_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    pick_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    sale_sku_code = CharField(null=True)
    sale_sku_img = CharField(null=True)
    sale_sku_name = CharField(null=True)
    sku_code = CharField(constraints=[SQL("DEFAULT ''")])
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    sort_no = IntegerField(null=True)
    source_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    transport_mode = IntegerField(null=True)
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'tdo_delivery_pick_detail'


class TdoDeliveryReceiptInfo(BaseModel):
    address = CharField(null=True)
    area = CharField(null=True)
    city = CharField(null=True)
    country = CharField(null=True)
    country_code = CharField(null=True)
    country_id = IntegerField(null=True)
    customer_type = IntegerField(null=True)
    delivery_order_code = CharField(index=True)
    delivery_order_id = BigIntegerField(index=True)
    email = CharField(null=True)
    first_name = CharField(null=True)
    id = BigAutoField()
    identity_card = CharField(null=True)
    last_name = CharField(null=True)
    phone = CharField(null=True)
    postcode = CharField(null=True)
    province = CharField(null=True)
    province_code = CharField(null=True)
    province_id = IntegerField(null=True)
    receipt_data = TextField(null=True)

    class Meta:
        table_name = 'tdo_delivery_receipt_info'


class TdoDeliveryStockDetail(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_order_code = CharField(index=True)
    delivery_order_detail_id = BigIntegerField(null=True)
    delivery_order_id = BigIntegerField(index=True)
    id = BigAutoField()
    location_code = CharField()
    location_id = BigIntegerField()
    operation_time = DateTimeField(null=True)
    operation_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    operation_username = CharField(null=True)
    pick_qty = IntegerField(null=True)
    sale_sku_code = CharField(null=True)
    sku_code = CharField()
    sku_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    warehouse_area_code = CharField()
    warehouse_area_id = BigIntegerField(null=True)
    warehouse_id = BigIntegerField(index=True)

    class Meta:
        table_name = 'tdo_delivery_stock_detail'


class TdoExpressOrder(BaseModel):
    bar_code = CharField(null=True)
    channel_code = CharField(null=True)
    channel_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    channel_name = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_order_code = CharField(index=True)
    delivery_order_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    express_order_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    ext_info = CharField(null=True)
    file_detail = TextField(null=True)
    file_path = TextField(null=True)
    id = BigAutoField()
    logistics_code = CharField(null=True)
    logistics_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    logistics_name = CharField(null=True)
    print_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    remarks = CharField(null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    warehouse_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'tdo_express_order'


class TdoExternalInterfaceOperateLog(BaseModel):
    create_time = DateTimeField()
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    create_username = CharField(constraints=[SQL("DEFAULT '0'")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    interface_flag = IntegerField()
    remark = CharField(null=True)
    request_content = TextField()
    request_time = DateTimeField(null=True)
    response_content = TextField(null=True)
    response_flag = IntegerField(constraints=[SQL("DEFAULT 1")])
    response_time = DateTimeField(null=True)
    source_order_code = CharField(constraints=[SQL("DEFAULT ''")])
    source_order_flag = IntegerField()
    source_order_id = BigIntegerField()
    system_flag = IntegerField()
    trace_id = CharField(constraints=[SQL("DEFAULT '0'")])
    transaction_commit_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'tdo_external_interface_operate_log'


class TdoHandoverOrder(BaseModel):
    create_time = DateTimeField()
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    handover_order_code = CharField(unique=True)
    handover_order_state = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    handover_time = DateTimeField(null=True)
    handover_user_id = BigIntegerField(null=True)
    handover_username = CharField(null=True)
    id = BigAutoField()
    print_time = DateTimeField(null=True)
    print_user_id = BigIntegerField(null=True)
    print_username = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'tdo_handover_order'


class TdoHandoverOrderDetail(BaseModel):
    car_number = CharField(null=True)
    channel_code = CharField(null=True)
    channel_name = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_order_code = CharField()
    delivery_order_id = BigIntegerField(index=True)
    express_order_id = BigIntegerField(index=True)
    handover_order_id = BigIntegerField(index=True)
    handover_order_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    logistics_code = CharField(null=True)
    logistics_name = CharField(null=True)
    scan_total = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tdo_handover_order_detail'


class TdoInterceptCancelOrder(BaseModel):
    create_time = DateTimeField(index=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_order_code = CharField(index=True)
    delivery_order_id = BigIntegerField(index=True)
    delivery_order_state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    handler_time = DateTimeField(null=True)
    handler_user_id = BigIntegerField(null=True)
    handler_username = CharField(null=True)
    id = BigAutoField()
    intercept_cancel_order_code = CharField(unique=True)
    intercept_cancel_order_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    intercept_cancel_order_type = IntegerField(null=True)
    reset_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(index=True, null=True)

    class Meta:
        table_name = 'tdo_intercept_cancel_order'


class TdoInterceptCancelOrderDetail(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    intercept_cancel_order_id = BigIntegerField(index=True)
    location_code = CharField(null=True)
    location_id = BigIntegerField(null=True)
    sale_sku_code = CharField()
    sale_sku_img = CharField(null=True)
    sale_sku_name = CharField()
    sku_code = CharField()
    sku_name = CharField()
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    warehouse_area_code = CharField(null=True)
    warehouse_area_id = BigIntegerField(null=True)
    warehouse_code = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'tdo_intercept_cancel_order_detail'


class TdoPackageTask(BaseModel):
    callback_content = TextField(null=True)
    callback_state = IntegerField(null=True)
    callback_time = DateTimeField(null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_order_code = CharField()
    delivery_order_id = BigIntegerField()
    id = BigAutoField()
    task_type = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tdo_package_task'


class TdoPickOrder(BaseModel):
    create_time = DateTimeField()
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    distribute_state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    pick_end_time = DateTimeField(null=True)
    pick_mode = IntegerField()
    pick_order_code = CharField(unique=True)
    pick_order_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    pick_start_time = DateTimeField(null=True)
    pick_type = IntegerField()
    pick_user_id = BigIntegerField(null=True)
    pick_username = CharField(null=True)
    print_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    prod_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    quality_time = DateTimeField(null=True)
    quality_user_id = BigIntegerField(null=True)
    quality_username = CharField(null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], index=True)

    class Meta:
        table_name = 'tdo_pick_order'


class TdoPickOrderDetail(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    location_code = CharField(null=True)
    location_id = BigIntegerField(null=True)
    pick_order_id = BigIntegerField(index=True)
    pick_qty = IntegerField(null=True)
    sku_code = CharField(null=True)
    sku_qty = IntegerField(null=True)
    warehouse_area_code = CharField(null=True)
    warehouse_id = BigIntegerField(index=True)

    class Meta:
        table_name = 'tdo_pick_order_detail'


class TrfBoxDemandDetail(BaseModel):
    box_detail_id = BigIntegerField(null=True)
    box_id = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    demand_code = CharField(null=True)
    demand_detail_id = BigIntegerField(null=True)
    demand_id = BigIntegerField(null=True)
    id = BigAutoField()
    sku_qty = IntegerField(null=True)

    class Meta:
        table_name = 'trf_box_demand_detail'


class TrfBoxOrder(BaseModel):
    box_no = CharField(index=True, null=True)
    box_remark = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_target_warehouse_code = CharField(null=True)
    delivery_target_warehouse_id = BigIntegerField(null=True)
    delivery_target_warehouse_name = CharField(null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(null=True)
    handover_id = BigIntegerField(null=True)
    handover_no = CharField(null=True)
    id = BigAutoField()
    in_state = IntegerField(null=True)
    out_state = IntegerField(null=True)
    print_state = IntegerField(null=True)
    process_result = CharField(null=True)
    receive_target_warehouse_code = CharField(null=True)
    receive_target_warehouse_id = BigIntegerField(null=True)
    receive_target_warehouse_name = CharField(null=True)
    receive_time = DateTimeField(null=True)
    receive_user_id = BigIntegerField(null=True)
    receive_username = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    sku_qty = IntegerField(null=True)
    storage_location_code = CharField(null=True)
    storage_location_id = BigIntegerField()
    transfer_in_id = BigIntegerField(null=True)
    transfer_in_no = CharField(null=True)
    transfer_out_id = BigIntegerField(null=True)
    transfer_out_no = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    volume = DecimalField(null=True)
    warehouse_id = BigIntegerField()
    weight = DecimalField(null=True)

    class Meta:
        table_name = 'trf_box_order'


class TrfBoxOrderDetail(BaseModel):
    bom_version = CharField(null=True)
    box_no = CharField(null=True)
    box_order_id = BigIntegerField(index=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    goods_sku_code = CharField()
    goods_sku_img = CharField(null=True)
    goods_sku_map = IntegerField(null=True)
    goods_sku_name = CharField(null=True)
    id = BigAutoField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    warehouse_id = BigIntegerField()
    wares_sku_code = CharField()
    wares_sku_name = CharField(null=True)
    wares_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'trf_box_order_detail'


class TrfBoxOrderDetailIn(BaseModel):
    box_no = CharField(null=True)
    box_order_id = BigIntegerField(index=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    goods_sku_code = CharField()
    goods_sku_img = CharField(null=True)
    goods_sku_name = CharField(null=True)
    id = BigAutoField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    warehouse_id = BigIntegerField()
    wares_sku_code = CharField()
    wares_sku_name = CharField(null=True)
    wares_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'trf_box_order_detail_in'


class TrfBoxOrderIn(BaseModel):
    box_no = CharField(index=True, null=True)
    box_remark = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(null=True)
    handover_id = BigIntegerField(null=True)
    handover_no = CharField(null=True)
    id = BigAutoField()
    print_state = IntegerField(null=True)
    process_result = CharField(null=True)
    receive_time = DateTimeField(null=True)
    receive_user_id = BigIntegerField(null=True)
    receive_username = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    sku_qty = IntegerField(null=True)
    state = IntegerField(null=True)
    transfer_in_id = BigIntegerField(null=True)
    transfer_in_no = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    volume = DecimalField(null=True)
    warehouse_id = BigIntegerField()
    weight = DecimalField(null=True)

    class Meta:
        table_name = 'trf_box_order_in'


class TrfDemandPickRelation(BaseModel):
    block_book_id = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    demand_code = CharField()
    demand_id = BigIntegerField(null=True)
    id = BigAutoField()
    pick_order_id = BigIntegerField(null=True)
    pick_order_no = CharField(constraints=[SQL("DEFAULT '0'")])
    priority = IntegerField(null=True)
    update_time = DateTimeField(null=True)

    class Meta:
        table_name = 'trf_demand_pick_relation'


class TrfHandoverOrder(BaseModel):
    box_qty = IntegerField(null=True)
    container_no = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_time = DateTimeField(null=True)
    delivery_user_id = BigIntegerField(null=True)
    delivery_username = CharField(null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(null=True)
    eta = DateTimeField(null=True)
    express_type = IntegerField(null=True)
    handover_no = CharField(index=True, null=True)
    handover_time = DateTimeField(null=True)
    id = BigAutoField()
    logistics_merchant = CharField(null=True)
    logistics_no = CharField(null=True)
    receive_state = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    receive_time = DateTimeField(null=True)
    receive_user_id = BigIntegerField(null=True)
    receive_username = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    remark = CharField(null=True)
    state = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'trf_handover_order'


class TrfPickDemandDetail(BaseModel):
    actual_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    demand_code = CharField(null=True)
    demand_detail_id = BigIntegerField(null=True)
    demand_id = BigIntegerField(null=True)
    expect_qty = IntegerField(null=True)
    id = BigAutoField()
    pick_detail_id = BigIntegerField(null=True)
    pick_order_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'trf_pick_demand_detail'


class TrfShelvesOrder(BaseModel):
    block_book_id = CharField(null=True)
    box_order_id = BigIntegerField()
    box_order_no = CharField()
    create_time = DateTimeField(index=True)
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_warehouse_id = BigIntegerField()
    id = BigAutoField()
    shelves_order_code = CharField(index=True)
    shelves_time = DateTimeField(null=True)
    shelves_user = BigIntegerField(null=True)
    shelves_username = CharField(null=True)
    stock_book_id = CharField(null=True)
    sync_ims = IntegerField(null=True)
    transfer_in_id = BigIntegerField()
    transfer_in_no = CharField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'trf_shelves_order'


class TrfShelvesOrder1(BaseModel):
    block_book_id = CharField(null=True)
    box_order_id = BigIntegerField()
    box_order_no = CharField()
    create_time = DateTimeField(index=True)
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField()
    del_flag = IntegerField(null=True)
    delivery_warehouse_id = BigIntegerField()
    id = BigAutoField()
    shelves_order_code = CharField(index=True)
    shelves_time = DateTimeField(null=True)
    shelves_user = BigIntegerField(null=True)
    shelves_username = CharField(null=True)
    stock_book_id = CharField(null=True)
    sync_ims = IntegerField(null=True)
    transfer_in_id = BigIntegerField()
    transfer_in_no = CharField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'trf_shelves_order1'


class TrfShelvesOrderDetail(BaseModel):
    bom_version = CharField(null=True)
    create_time = DateTimeField()
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    create_username = CharField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    goods_sku_code = CharField(null=True)
    goods_sku_map = IntegerField(null=True)
    goods_sku_name = CharField(null=True)
    id = BigAutoField()
    qty = IntegerField(null=True)
    shelves_order_code = CharField(null=True)
    shelves_order_id = BigIntegerField(index=True, null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_location_code = CharField()
    warehouse_location_id = BigIntegerField(index=True)
    wares_sku_code = CharField(null=True)
    wares_sku_name = CharField(null=True)

    class Meta:
        table_name = 'trf_shelves_order_detail'


class TrfTransferDemand(BaseModel):
    block_book_id = CharField(null=True)
    box_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    cancel_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    cancel_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    category_id = BigIntegerField(null=True)
    category_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    customer_remark = CharField(null=True)
    customer_type = IntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_target_warehouse_code = CharField(null=True)
    delivery_target_warehouse_id = BigIntegerField(null=True)
    delivery_target_warehouse_name = CharField(null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_name = CharField(null=True)
    demand_code = CharField(index=True, null=True)
    demand_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    demand_type = IntegerField(null=True)
    distribute_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_code = CharField()
    goods_sku_en_name = CharField(null=True)
    goods_sku_img = CharField(null=True)
    goods_sku_name = CharField(null=True)
    id = BigAutoField()
    receive_target_warehouse_code = CharField(null=True)
    receive_target_warehouse_id = BigIntegerField(null=True)
    receive_target_warehouse_name = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    sale_order_code = CharField(null=True)
    source_code = CharField(null=True)
    state = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    volume = DecimalField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'trf_transfer_demand'


class TrfTransferDemandDetail(BaseModel):
    bom_version = CharField(null=True)
    cancel_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    demand_code = CharField(index=True)
    demand_id = BigIntegerField(index=True)
    distribute_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_code = CharField()
    goods_sku_img = CharField(null=True)
    goods_sku_map = IntegerField(null=True)
    goods_sku_name = CharField(null=True)
    id = BigAutoField()
    in_transit_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    receipt_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    update_time = DateTimeField(null=True)
    warehouse_id = BigIntegerField()
    wares_sku_code = CharField(index=True)
    wares_sku_name = CharField()
    wares_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'trf_transfer_demand_detail'


class TrfTransferInDemandDetail(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    demand_code = CharField(null=True)
    demand_detail_id = BigIntegerField(null=True)
    demand_id = BigIntegerField(null=True)
    id = BigAutoField()
    receivee_qty = IntegerField(null=True)
    shelves_qty = IntegerField(null=True)
    transfer_detail_id = BigIntegerField(null=True)
    transfer_in_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'trf_transfer_in_demand_detail'


class TrfTransferInOrder(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_target_warehouse_code = CharField(null=True)
    delivery_target_warehouse_id = BigIntegerField(null=True)
    delivery_target_warehouse_name = CharField(null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(null=True)
    goods_sku_kind_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    handover_id = BigIntegerField()
    handover_no = CharField()
    id = BigAutoField()
    receive_target_warehouse_code = CharField(null=True)
    receive_target_warehouse_id = BigIntegerField(null=True)
    receive_target_warehouse_name = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    transfer_in_no = CharField(index=True)
    transfer_out_id = BigIntegerField()
    transfer_out_no = CharField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField()
    wares_sku_kind_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    wares_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    wares_sku_shelf_qty = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'trf_transfer_in_order'


class TrfTransferInOrderDetail(BaseModel):
    bom_version = CharField(null=True)
    box_no = CharField(null=True)
    box_order_id = BigIntegerField(index=True, null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    goods_sku_code = CharField()
    goods_sku_img = CharField(null=True)
    goods_sku_map = IntegerField(null=True)
    goods_sku_name = CharField(null=True)
    id = BigAutoField()
    transfer_in_id = BigIntegerField(index=True)
    transfer_in_no = CharField(index=True, null=True)
    update_time = DateTimeField(null=True)
    warehouse_id = BigIntegerField()
    wares_sku_code = CharField()
    wares_sku_exception_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    wares_sku_name = CharField(null=True)
    wares_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    wares_sku_receipt_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    wares_sku_shelf_qty = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'trf_transfer_in_order_detail'


class TrfTransferOrderOperateLog(BaseModel):
    content = TextField()
    create_time = DateTimeField()
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    id = BigAutoField()
    operate_type = IntegerField()
    remark = CharField(null=True)
    result_content = TextField(null=True)
    trace_id = CharField(null=True)

    class Meta:
        table_name = 'trf_transfer_order_operate_log'


class TrfTransferOutOrder(BaseModel):
    change_time = DateTimeField(null=True)
    change_user_id = BigIntegerField(null=True)
    change_username = CharField(null=True)
    complete_flag = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    del_time = DateTimeField(null=True)
    del_user_id = BigIntegerField(null=True)
    del_username = CharField(null=True)
    delivery_target_warehouse_code = CharField(null=True)
    delivery_target_warehouse_id = BigIntegerField(null=True)
    delivery_target_warehouse_name = CharField(null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(null=True)
    goods_sku_kind_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    handover_id = BigIntegerField(null=True)
    handover_no = CharField(null=True)
    id = BigAutoField()
    paternity = CharField(null=True)
    receive_target_warehouse_code = CharField(null=True)
    receive_target_warehouse_id = BigIntegerField(null=True)
    receive_target_warehouse_name = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    remark = CharField(null=True)
    source_transfer_out_id = BigIntegerField(null=True)
    source_transfer_out_no = CharField(null=True)
    split_time = DateTimeField(null=True)
    split_user_id = BigIntegerField(null=True)
    split_username = CharField(null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")])
    transfer_out_no = CharField(null=True, unique=True)
    type = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField()
    wares_sku_kind_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    wares_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'trf_transfer_out_order'


class TrfTransferOutOrderDetail(BaseModel):
    bom_version = CharField(null=True)
    box_no = CharField(null=True)
    box_order_id = BigIntegerField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    goods_sku_code = CharField()
    goods_sku_img = CharField(null=True)
    goods_sku_map = IntegerField(null=True)
    goods_sku_name = CharField(null=True)
    id = BigAutoField()
    transfer_out_id = BigIntegerField(index=True)
    transfer_out_no = CharField(index=True, null=True)
    update_time = DateTimeField(null=True)
    warehouse_id = BigIntegerField()
    wares_sku_code = CharField()
    wares_sku_name = CharField(null=True)
    wares_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'trf_transfer_out_order_detail'


class TrfTransferPickOrder(BaseModel):
    block_book_id = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], index=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_target_warehouse_code = CharField(null=True)
    delivery_target_warehouse_id = BigIntegerField(null=True)
    delivery_target_warehouse_name = CharField(null=True)
    delivery_warehouse_code = CharField()
    delivery_warehouse_name = CharField()
    goods_type = IntegerField()
    id = BigAutoField()
    pick_order_no = CharField(index=True)
    pick_order_type = IntegerField()
    pick_time = DateTimeField(null=True)
    pick_type = IntegerField()
    pick_user_id = BigIntegerField(null=True)
    pick_username = CharField(null=True)
    print_count = IntegerField(constraints=[SQL("DEFAULT 0")])
    receive_target_warehouse_code = CharField(null=True)
    receive_target_warehouse_id = BigIntegerField(null=True)
    receive_target_warehouse_name = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    state = IntegerField()
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField()
    work_type = IntegerField(null=True)

    class Meta:
        table_name = 'trf_transfer_pick_order'


class TrfTransferPickOrderDetail(BaseModel):
    bom_version = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    goods_sku_code = CharField()
    goods_sku_en_name = CharField(null=True)
    goods_sku_img = CharField(null=True)
    goods_sku_map = IntegerField(null=True)
    goods_sku_name = CharField()
    id = BigAutoField()
    pick_order_id = BigIntegerField(index=True)
    pick_order_no = CharField(index=True, null=True)
    real_pick_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    should_pick_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    storage_location_code = CharField(null=True)
    storage_location_id = BigIntegerField()
    update_time = DateTimeField(null=True)
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    wares_sku_code = CharField()
    wares_sku_name = CharField()

    class Meta:
        table_name = 'trf_transfer_pick_order_detail'


class TrfTransferPickTrayRelation(BaseModel):
    box_check_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    divert_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    exception_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    pick_order_id = BigIntegerField(index=True)
    pick_order_no = CharField(index=True)
    storage_location_code = CharField()
    storage_location_id = BigIntegerField()
    tray_sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'trf_transfer_pick_tray_relation'


class TrfTransferPickTrayRelationDetail(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    from_loc_code = CharField(null=True)
    from_loc_id = BigIntegerField(null=True)
    goods_sku_code = CharField()
    goods_sku_name = CharField()
    id = BigAutoField()
    pick_tray_relation_id = BigIntegerField()
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    to_loc_code = CharField(null=True)
    to_loc_id = BigIntegerField(null=True)
    type = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField()
    wares_sku_code = CharField()
    wares_sku_name = CharField()

    class Meta:
        table_name = 'trf_transfer_pick_tray_relation_detail'


class TsfEntryOrder(BaseModel):
    category = IntegerField(null=True)
    create_time = DateTimeField(index=True, null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(null=True)
    entry_order_code = CharField(unique=True)
    id = BigAutoField()
    receive_target_warehouse_code = CharField(null=True)
    receive_target_warehouse_id = BigIntegerField(null=True)
    receive_target_warehouse_name = CharField(null=True)
    receive_time = DateTimeField(null=True)
    receive_user_id = BigIntegerField(null=True)
    receive_username = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    remarks = CharField(null=True)
    source_order_code = CharField(index=True, null=True)
    state = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'tsf_entry_order'


class TsfEntryOrderDetail(BaseModel):
    bom_map = IntegerField(null=True)
    bom_version = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    entry_order_code = CharField(index=True)
    entry_order_id = BigIntegerField(index=True)
    exception_qty = IntegerField(null=True)
    id = BigAutoField()
    sale_sku_code = CharField()
    sale_sku_name = CharField(null=True)
    shelf_qty = IntegerField(null=True)
    sku_code = CharField()
    sku_name = CharField(null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tsf_entry_order_detail'


class TsfEntryOrderPack(BaseModel):
    box_order_code = CharField(index=True)
    box_order_id = BigIntegerField(index=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    entry_order_code = CharField(index=True)
    entry_order_id = BigIntegerField(index=True)
    id = BigAutoField()
    state = BigIntegerField(null=True)

    class Meta:
        table_name = 'tsf_entry_order_pack'


class TsfEntryOrderPackDetail(BaseModel):
    bom_map = IntegerField(null=True)
    bom_version = CharField(null=True)
    box_order_code = CharField(index=True)
    box_order_detail_id = BigIntegerField(index=True)
    box_order_id = BigIntegerField(index=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    entry_order_code = CharField(index=True)
    entry_order_detail_id = BigIntegerField(index=True)
    entry_order_id = BigIntegerField(index=True)
    exception_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    sale_sku_code = CharField()
    sale_sku_name = CharField(null=True)
    shelf_qty = IntegerField(null=True)
    sku_code = CharField()
    sku_name = CharField(null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'tsf_entry_order_pack_detail'


class TsfInstructHandoverOrder(BaseModel):
    category = IntegerField(null=True)
    container_no = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_time = DateTimeField(null=True)
    delivery_user_id = BigIntegerField(null=True)
    delivery_username = CharField(null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(null=True)
    eta = DateTimeField(null=True)
    express_type = IntegerField(null=True)
    handover_no = CharField(index=True, null=True)
    id = BigAutoField()
    logistics_merchant = CharField(null=True)
    logistics_no = CharField(null=True)
    receive_state = IntegerField(null=True)
    receive_target_warehouse_code = CharField(null=True)
    receive_target_warehouse_id = BigIntegerField(null=True)
    receive_target_warehouse_name = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    remark = CharField(null=True)
    state = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'tsf_instruct_handover_order'


class TsfInstructHandoverOrderDetail(BaseModel):
    box_id = BigIntegerField(index=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    handover_order_id = BigIntegerField(index=True)
    id = BigAutoField()

    class Meta:
        table_name = 'tsf_instruct_handover_order_detail'


class TsfInstructHandoverOrderProp(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    handover_order_id = BigIntegerField(index=True)
    handover_order_no = CharField(index=True, null=True)
    id = BigAutoField()
    prop_code = CharField(index=True, null=True)
    prop_id = BigIntegerField(null=True)
    prop_name = CharField(null=True)
    prop_value = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'tsf_instruct_handover_order_prop'
        indexes = (
            (('handover_order_id', 'prop_id'), False),
        )


class TsfInstructOrder(BaseModel):
    block_book_id = CharField(null=True)
    cancel_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    category = IntegerField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_target_warehouse_code = CharField(null=True)
    delivery_target_warehouse_id = BigIntegerField(null=True)
    delivery_target_warehouse_name = CharField(null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(null=True)
    id = BigAutoField()
    instruct_order_no = CharField(index=True)
    part_cancel_flag = IntegerField(null=True)
    receive_target_warehouse_code = CharField(null=True)
    receive_target_warehouse_id = BigIntegerField(null=True)
    receive_target_warehouse_name = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    remark = CharField(null=True)
    source_order_no = CharField(index=True, null=True)
    state = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'tsf_instruct_order'


class TsfInstructOrderDetail(BaseModel):
    bom_map = IntegerField(null=True)
    bom_version = CharField(null=True)
    cancel_qty = IntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_qty = IntegerField(null=True)
    extension = CharField(null=True)
    height = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    id = BigAutoField()
    instruct_order_id = BigIntegerField(index=True)
    instruct_order_no = CharField(index=True)
    length = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    priority = IntegerField(null=True)
    sale_sku_code = CharField()
    sale_sku_img = CharField(null=True)
    sale_sku_name = CharField(null=True)
    short_pick = IntegerField(null=True)
    sku_code = CharField()
    sku_name = CharField(null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    weight = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    width = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)

    class Meta:
        table_name = 'tsf_instruct_order_detail'


class TsfInstructOrderProp(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    instruct_order_id = BigIntegerField(index=True)
    instruct_order_no = CharField(index=True, null=True)
    prop_code = CharField(index=True, null=True)
    prop_id = BigIntegerField(index=True, null=True)
    prop_name = CharField(null=True)
    prop_value = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'tsf_instruct_order_prop'
        indexes = (
            (('instruct_order_id', 'prop_id'), False),
        )


class TsfPackOrder(BaseModel):
    box_order_no = CharField(index=True, null=True)
    category = IntegerField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(null=True)
    height = DecimalField(null=True)
    id = BigAutoField()
    length = DecimalField(null=True)
    location_code = CharField(null=True)
    location_id = BigIntegerField()
    parent_order_id = BigIntegerField(null=True)
    parent_order_no = CharField(null=True)
    pick_order_id = BigIntegerField(index=True)
    pick_order_no = CharField(index=True, null=True)
    receive_target_warehouse_code = CharField(null=True)
    receive_target_warehouse_id = BigIntegerField(null=True)
    receive_target_warehouse_name = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    remark = CharField(null=True)
    sku_qty = IntegerField(null=True)
    state = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    volume = DecimalField(null=True)
    warehouse_id = BigIntegerField()
    weight = DecimalField(null=True)
    width = DecimalField(null=True)

    class Meta:
        table_name = 'tsf_pack_order'


class TsfPackOrderDetail(BaseModel):
    bom_map = IntegerField(null=True)
    bom_version = CharField(null=True)
    box_order_id = BigIntegerField(index=True)
    box_order_no = CharField(index=True, null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    height = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    id = BigAutoField()
    length = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    sale_sku_code = CharField()
    sale_sku_img = CharField(null=True)
    sale_sku_name = CharField(null=True)
    sku_code = CharField()
    sku_name = CharField(null=True)
    sku_qty = IntegerField()
    weight = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    width = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)

    class Meta:
        table_name = 'tsf_pack_order_detail'


class TsfPackOrderInstructDetail(BaseModel):
    bom_map = IntegerField()
    bom_version = CharField()
    box_order_detail_id = BigIntegerField(index=True)
    box_order_id = BigIntegerField(index=True, null=True)
    box_order_no = CharField(index=True, null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_target_warehouse_code = CharField(null=True)
    delivery_target_warehouse_id = BigIntegerField(null=True)
    delivery_target_warehouse_name = CharField(null=True)
    height = DecimalField(null=True)
    id = BigAutoField()
    instruct_order_detail_id = BigIntegerField(index=True)
    instruct_order_id = BigIntegerField(index=True, null=True)
    instruct_order_no = CharField(index=True, null=True)
    length = DecimalField(null=True)
    sale_sku_code = CharField()
    sale_sku_img = CharField(null=True)
    sale_sku_name = CharField(null=True)
    sku_code = CharField()
    sku_name = CharField(null=True)
    sku_qty = IntegerField()
    weight = DecimalField(null=True)
    width = DecimalField(null=True)

    class Meta:
        table_name = 'tsf_pack_order_instruct_detail'


class TsfPickInstructRel(BaseModel):
    block_book_id = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    instruct_order_id = BigIntegerField(index=True, null=True)
    instruct_order_no = CharField(index=True)
    pick_order_id = BigIntegerField(index=True)
    pick_order_no = CharField(index=True)
    priority = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'tsf_pick_instruct_rel'


class TsfPickOrder(BaseModel):
    assign_strategy = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    block_strategy = IntegerField(null=True)
    category = IntegerField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_warehouse_code = CharField(null=True)
    delivery_warehouse_id = BigIntegerField(null=True)
    delivery_warehouse_name = CharField(null=True)
    fetch_time = DateTimeField(null=True)
    finish_time = DateTimeField(null=True)
    id = BigAutoField()
    pack_state = IntegerField(constraints=[SQL("DEFAULT 0")])
    pick_mode = IntegerField(null=True)
    pick_order_no = CharField(index=True)
    print_count = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    receive_target_warehouse_code = CharField(null=True)
    receive_target_warehouse_id = BigIntegerField(null=True)
    receive_target_warehouse_name = CharField(null=True)
    receive_warehouse_code = CharField(null=True)
    receive_warehouse_id = BigIntegerField(null=True)
    receive_warehouse_name = CharField(null=True)
    sku_qty = IntegerField()
    state = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    volume = DecimalField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'tsf_pick_order'


class TsfPickOrderDetail(BaseModel):
    bom_map = IntegerField(null=True)
    bom_version = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    height = DecimalField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    length = DecimalField(constraints=[SQL("DEFAULT 0")], null=True)
    location_code = CharField(index=True)
    location_id = BigIntegerField(index=True)
    pick_order_id = BigIntegerField(index=True)
    pick_order_no = CharField(index=True)
    pick_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    sale_sku_code = CharField(null=True)
    sale_sku_img = CharField(null=True)
    sale_sku_name = CharField(null=True)
    sku_code = CharField()
    sku_name = CharField(null=True)
    sku_qty = IntegerField()
    weight = DecimalField(constraints=[SQL("DEFAULT 0")], null=True)
    width = DecimalField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'tsf_pick_order_detail'


class TsfPickOrderInstructDetail(BaseModel):
    bom_map = IntegerField()
    bom_version = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    delivery_target_warehouse_code = CharField(null=True)
    delivery_target_warehouse_id = BigIntegerField(null=True)
    delivery_target_warehouse_name = CharField(null=True)
    id = BigAutoField()
    instruct_order_detail_id = BigIntegerField(index=True, null=True)
    instruct_order_id = BigIntegerField(index=True, null=True)
    instruct_order_no = CharField(index=True, null=True)
    location_code = CharField(index=True, null=True)
    location_id = BigIntegerField(index=True, null=True)
    pick_order_detail_id = BigIntegerField(index=True)
    pick_order_id = BigIntegerField(index=True)
    pick_order_no = CharField(index=True, null=True)
    pick_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sale_sku_code = CharField(null=True)
    sale_sku_name = CharField(null=True)
    sku_code = CharField(null=True)
    sku_name = CharField(null=True)
    sku_qty = IntegerField()

    class Meta:
        table_name = 'tsf_pick_order_instruct_detail'


class TsfPickOrderInventory(BaseModel):
    del_flag = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    location_code = CharField(index=True, null=True)
    location_id = BigIntegerField(index=True)
    packed_qty = IntegerField(null=True)
    pick_order_id = BigIntegerField(index=True)
    pick_order_no = CharField(index=True, null=True)
    sku_qty = IntegerField(null=True)
    warehouse_id = BigIntegerField()

    class Meta:
        table_name = 'tsf_pick_order_inventory'


class TsfPickOrderInventoryDetail(BaseModel):
    abnormal_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    bom_map = IntegerField(null=True)
    bom_version = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    location_code = CharField(index=True, null=True)
    location_id = BigIntegerField(index=True, null=True)
    packed_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    pick_order_id = BigIntegerField(index=True, null=True)
    pick_order_no = CharField(index=True, null=True)
    sale_sku_code = CharField(null=True)
    sale_sku_name = CharField(null=True)
    sku_code = CharField()
    sku_name = CharField(null=True)
    sku_qty = IntegerField()

    class Meta:
        table_name = 'tsf_pick_order_inventory_detail'


class TsfPickOrderInventoryMovement(BaseModel):
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    dest_location_code = CharField(null=True)
    dest_location_id = BigIntegerField()
    dest_location_type = IntegerField(null=True)
    id = BigAutoField()
    operate_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    operate_type = IntegerField(null=True)
    operate_user_id = BigIntegerField(null=True)
    operate_username = CharField(null=True)
    pick_order_id = BigIntegerField(index=True)
    pick_order_no = CharField(null=True)
    sku_code = CharField()
    sku_name = CharField()
    source_location_code = CharField(null=True)
    source_location_id = BigIntegerField()
    source_location_type = IntegerField(null=True)

    class Meta:
        table_name = 'tsf_pick_order_inventory_movement'


class TsfPickOrderPicker(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    pick_order_id = BigIntegerField(index=True, null=True)
    pick_order_no = CharField(index=True, null=True)
    pick_user_id = BigIntegerField(index=True, null=True)
    pick_username = CharField(null=True)

    class Meta:
        table_name = 'tsf_pick_order_picker'


class TsfPropKeyDict(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    prop_code = CharField(unique=True)
    prop_name = CharField(null=True)
    remark = CharField(null=True)
    type = IntegerField(null=True)

    class Meta:
        table_name = 'tsf_prop_key_dict'


class TsfShelvesOrder(BaseModel):
    block_book_id = CharField(null=True)
    box_order_code = CharField(null=True)
    box_order_id = BigIntegerField(null=True)
    create_time = DateTimeField(index=True, null=True)
    create_user_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    entry_order_id = BigIntegerField(index=True)
    entry_order_no = CharField(index=True)
    id = BigAutoField()
    shelves_order_code = CharField(index=True)
    shelves_time = DateTimeField(null=True)
    shelves_user_id = BigIntegerField(null=True)
    shelves_username = CharField(null=True)
    stock_book_id = CharField(null=True)
    sync_ims = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    warehouse_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'tsf_shelves_order'


class TsfShelvesOrderDetail(BaseModel):
    bom_map = IntegerField(null=True)
    bom_version = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    location_code = CharField(index=True, null=True)
    location_id = BigIntegerField(index=True, null=True)
    sale_sku_code = CharField(null=True)
    sale_sku_name = CharField(null=True)
    shelves_order_id = BigIntegerField(index=True, null=True)
    shelves_order_no = CharField(index=True, null=True)
    sku_code = CharField(null=True)
    sku_name = CharField(null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'tsf_shelves_order_detail'


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


class WarehouseSkuRelation(BaseModel):
    bom_version = CharField(null=True)
    create_time = DateTimeField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], index=True)
    id = BigAutoField()
    location_code = CharField(constraints=[SQL("DEFAULT ''")])
    location_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])
    relation_order_code = CharField(index=True, null=True)
    relation_order_id = BigIntegerField(index=True)
    relation_order_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    sale_sku_code = CharField(index=True)
    sale_sku_name = CharField(null=True)
    shelves_time = DateTimeField(index=True, null=True)
    sku_code = CharField(constraints=[SQL("DEFAULT ''")], index=True)
    sku_name = CharField(null=True)
    sku_qty = IntegerField(constraints=[SQL("DEFAULT 0")])
    sku_stock = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(null=True)
    warehouse_area_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    warehouse_area_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    warehouse_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    warehouse_id = BigIntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'warehouse_sku_relation'
