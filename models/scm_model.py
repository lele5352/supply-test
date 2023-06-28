from peewee import *

from config import scms_db_config

database = MySQLDatabase('supply_scm', **scms_db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class HandlePlan(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    exception_detail_id = BigIntegerField(index=True)
    handle_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    handle_plan_type = IntegerField()
    handle_remark = CharField(null=True)
    handle_status = IntegerField()
    handle_time = DateTimeField(null=True)
    handle_user_id = BigIntegerField(null=True)
    handle_user_name = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    remark = CharField(null=True)
    ship_goods_remark = CharField(null=True)
    supplier_handle_status = IntegerField(null=True)
    supplier_handle_time = DateTimeField(null=True)
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    wares_sku = CharField()

    class Meta:
        table_name = 'handle_plan'


class ProductInfo(BaseModel):
    brand_id = IntegerField(null=True)
    category_id = IntegerField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField(null=True)
    create_user_name = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    height = DecimalField(null=True)
    id = BigAutoField()
    instruction_book_json = UnknownField(null=True)  # json
    length = DecimalField(null=True)
    main_url = CharField(null=True)
    part_sku_type = IntegerField(null=True)
    product_archive_url = CharField(null=True)
    product_create_time = DateTimeField(null=True)
    product_create_user = BigIntegerField(null=True)
    product_create_user_name = CharField(null=True)
    product_name_cn = CharField()
    product_name_en = CharField(null=True)
    purchase_price = DecimalField()
    sale_attr_name_cn = CharField(null=True)
    sale_attr_name_en = CharField(null=True)
    sku_code = CharField(unique=True)
    spu_code = CharField(null=True)
    status = IntegerField(constraints=[SQL("DEFAULT 1")])
    supplier_id = BigIntegerField()
    sync_time = DateTimeField(null=True)
    trace_id = CharField(null=True)
    type = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    weight = DecimalField(null=True)
    width = DecimalField(null=True)

    class Meta:
        table_name = 'product_info'


class ProductSkuLabel(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    label_id = BigIntegerField(index=True)
    sku_code = CharField(index=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user = BigIntegerField(null=True)
    value = CharField()

    class Meta:
        table_name = 'product_sku_label'


class PurchaseDemand(BaseModel):
    cancel_remark = CharField(null=True)
    cancel_time = DateTimeField(null=True)
    cancel_user_id = BigIntegerField(null=True)
    cancel_user_name = CharField(null=True)
    confirm_remark = CharField(null=True)
    confirm_time = DateTimeField(null=True)
    confirm_user_id = BigIntegerField(null=True)
    confirm_user_name = CharField(null=True)
    create_time = DateTimeField()
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    delivery_warehouse = CharField(index=True)
    destination_warehouse = CharField(null=True)
    exception_remark = CharField(null=True)
    exception_time = DateTimeField(null=True)
    exception_user_id = BigIntegerField(null=True)
    exception_user_name = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    online_order_number = CharField(null=True)
    order_number = CharField(index=True)
    purchase_demand_remark = CharField(null=True)
    purchase_demand_status = IntegerField()
    purchase_remark = CharField(null=True)
    purchase_type = IntegerField()
    quality_test_type = IntegerField()
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'purchase_demand'


class PurchaseDemandSkuInfo(BaseModel):
    bom_detail = UnknownField(null=True)  # json
    bom_id = BigIntegerField(null=True)
    bom_version = CharField(null=True)
    consult_date_of_delivery = DateTimeField(null=True)
    default_date_of_delivery = IntegerField(null=True)
    destination_warehouse = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField(index=True, null=True)
    market_sku_img = CharField(null=True)
    market_sku_label = IntegerField(null=True)
    market_sku_name_cn = CharField(null=True)
    market_sku_type = IntegerField(null=True)
    order_number = CharField(index=True, null=True)
    pdf = CharField(null=True)
    purchase_demand_id = BigIntegerField(index=True, null=True)
    purchase_price = DecimalField(null=True)
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ratio = DecimalField(null=True)
    remark = CharField(null=True)
    supplier_remark = CharField(null=True)
    total_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'purchase_demand_sku_info'


class PurchaseDemandSupplierInfo(BaseModel):
    advance_ratio = DecimalField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    payment_date = IntegerField(null=True)
    payment_period = IntegerField(null=True)
    payment_type = IntegerField(null=True)
    purchase_demand_id = BigIntegerField(index=True)
    purchaser_id = BigIntegerField(null=True)
    purchaser_name = CharField(null=True)
    settlement_method = IntegerField(null=True)
    supplier_info_id = BigIntegerField()
    supplier_name = CharField(null=True)
    trace_id = CharField(null=True)
    tracer_id = BigIntegerField(null=True)
    tracer_name = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'purchase_demand_supplier_info'


class PurchaseExceptionDetail(BaseModel):
    build_plan_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField(null=True)
    creator_name = CharField(null=True)
    exception_code = CharField(null=True)
    exception_description = CharField(null=True)
    exception_info_id = BigIntegerField(index=True)
    exception_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    exception_type = IntegerField()
    finish_time = DateTimeField(null=True)
    finish_user_id = BigIntegerField(null=True)
    finish_user_name = CharField(null=True)
    finished_plan_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    handle_time = DateTimeField(null=True)
    handle_user_id = BigIntegerField(null=True)
    handle_user_name = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    plan_status = IntegerField()
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    wares_sku = CharField()
    wares_sku_name_cn = CharField()

    class Meta:
        table_name = 'purchase_exception_detail'


class PurchaseExceptionImg(BaseModel):
    exception_detail_id = BigIntegerField(index=True)
    exception_img = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'purchase_exception_img'


class PurchaseExceptionInfo(BaseModel):
    bom_detail = UnknownField()  # json
    bom_id = IntegerField()
    bom_version = CharField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField(null=True)
    creator_name = CharField(null=True)
    exception_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    exception_order_code = CharField(null=True)
    exception_process = IntegerField(null=True)
    exception_status = IntegerField()
    handle_time = DateTimeField(null=True)
    handle_user_id = BigIntegerField(null=True)
    handle_user_name = CharField(null=True)
    id = BigAutoField()
    is_committed = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField(index=True)
    market_sku_img = CharField()
    market_sku_label = CharField(null=True)
    market_sku_name_cn = CharField()
    market_sku_type = IntegerField()
    purchase_order_id = BigIntegerField(index=True)
    purchase_order_no = CharField()
    purchaser_id = BigIntegerField()
    purchaser_name = CharField()
    sale_attr_name_cn = CharField(null=True)
    shipping_order_id = BigIntegerField(null=True)
    shipping_order_no = CharField(index=True, null=True)
    source = IntegerField(constraints=[SQL("DEFAULT 0")])
    supplier_exception_status = IntegerField(null=True)
    supplier_handle_time = DateTimeField(null=True)
    supplier_id = BigIntegerField()
    supplier_name = CharField()
    trace_id = CharField(null=True)
    tracer_id = BigIntegerField()
    tracer_name = CharField()
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    warehouse = CharField()

    class Meta:
        table_name = 'purchase_exception_info'
        indexes = (
            (('purchase_order_id', 'market_sku'), False),
        )


class PurchaseOrder(BaseModel):
    accept_supplier_id = BigIntegerField(null=True)
    accept_supplier_name = CharField(null=True)
    accept_time = DateTimeField(null=True)
    arrived_date_of_delivery = DateTimeField(null=True)
    cancel_remark = CharField(null=True)
    cancel_time = DateTimeField(null=True)
    cancel_user_id = BigIntegerField(null=True)
    cancel_user_name = CharField(null=True)
    confirm_remark = CharField(null=True)
    confirm_time = DateTimeField(null=True)
    confirm_user_id = BigIntegerField(null=True)
    confirm_user_name = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_user_name = CharField(null=True)
    delivery_status = IntegerField(null=True)
    delivery_warehouse = CharField(index=True, null=True)
    discount = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    finished_remark = CharField(null=True)
    finished_time = DateTimeField(null=True)
    finished_user_id = BigIntegerField(null=True)
    finished_user_name = CharField(null=True)
    freight = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_first_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    online_order_number = CharField(null=True)
    order_time = DateTimeField(null=True)
    order_user_id = BigIntegerField(null=True)
    order_user_name = CharField(null=True)
    purchase_number = CharField(null=True)
    purchase_order_status = IntegerField(null=True)
    purchase_remark = CharField(null=True)
    quality_test_type = IntegerField(null=True)
    supplier_accept_status = IntegerField(null=True)
    total_purchase_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    total_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'purchase_order'
        indexes = (
            (('purchase_number', 'is_deleted'), True),
        )


class PurchaseOrderIms(BaseModel):
    block_book_id = CharField(null=True)
    create_time = DateTimeField(null=True)
    id = BigAutoField()
    invoke_times = BigIntegerField(null=True)
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    operate_type = CharField(null=True)
    purchase_no = CharField(null=True)
    purchase_order_id = BigIntegerField(null=True)
    stock_book_id = CharField(null=True)
    trace_id = CharField(null=True)
    version = BigIntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'purchase_order_ims'


class PurchaseOrderPaymentInfo(BaseModel):
    account_dept = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    account_not_apply = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    account_not_paid = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    account_paid = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    actual_account_dept = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    exception_dept = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    payment_status = IntegerField(null=True)
    purchase_order_id = BigIntegerField(index=True, null=True)
    trace_id = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'purchase_order_payment_info'


class PurchaseOrderSkuInfo(BaseModel):
    actual_price = DecimalField(null=True)
    arrived_warehouse_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    arriving_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    bom_detail = UnknownField(null=True)  # json
    bom_id = IntegerField(null=True)
    bom_version = CharField(null=True)
    consult_date_of_delivery = DateField(null=True)
    default_date_of_delivery = IntegerField(null=True)
    destination_warehouse = CharField(index=True, null=True)
    exception_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    instruction_book_json = UnknownField(null=True)  # json
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_first_order = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField(index=True, null=True)
    market_sku_img = CharField(null=True)
    market_sku_label = CharField(null=True)
    market_sku_name_cn = CharField(null=True)
    market_sku_type = IntegerField(null=True)
    online_shopping_remark = CharField(null=True)
    online_shopping_url = CharField(null=True)
    order_number = CharField(index=True, null=True)
    pdf = CharField(null=True)
    purchase_demand_id = BigIntegerField(null=True)
    purchase_demand_time = DateTimeField(null=True)
    purchase_order_id = BigIntegerField(index=True, null=True)
    purchase_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    purchase_type = IntegerField(null=True)
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    ratio = DecimalField(null=True)
    remark = CharField(null=True)
    sale_attr_name_cn = CharField(null=True)
    supplier_item_no = CharField(null=True)
    supplier_remark = CharField(null=True)
    total_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")], null=True)
    trace_id = CharField(null=True)
    unshipped_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'purchase_order_sku_info'


class PurchaseOrderSupplierInfo(BaseModel):
    advance_ratio = DecimalField(null=True)
    audit_date = IntegerField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    payment_date = IntegerField(null=True)
    payment_period = IntegerField(null=True)
    payment_type = IntegerField(null=True)
    purchase_order_id = BigIntegerField(index=True, null=True)
    purchaser_id = BigIntegerField(null=True)
    purchaser_name = CharField(null=True)
    settlement_method = IntegerField(null=True)
    supplier_info_id = BigIntegerField(null=True)
    supplier_name = CharField(null=True)
    trace_id = CharField(null=True)
    tracer_id = BigIntegerField(null=True)
    tracer_name = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'purchase_order_supplier_info'


class PurchasePriceHistory(BaseModel):
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField()
    order_time = DateTimeField()
    orderer_id = IntegerField()
    orderer_name = CharField()
    purchase_order_id = BigIntegerField()
    purchase_order_no = CharField()
    purchase_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    supplier_info_id = BigIntegerField()
    supplier_name = CharField()
    trace_id = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'purchase_price_history'


class PurchaseSkuUrgentNumber(BaseModel):
    create_time = DateTimeField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField(index=True)
    purchase_order_id = BigIntegerField(index=True)
    purchase_order_no = CharField(index=True)
    stock_version = IntegerField()
    trace_id = CharField(null=True)
    urgent_number = IntegerField()
    version = IntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'purchase_sku_urgent_number'


class SettlementApply(BaseModel):
    apply_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    apply_no = CharField(unique=True)
    apply_status = IntegerField()
    apply_time = DateTimeField(null=True)
    apply_type = IntegerField()
    apply_user_id = BigIntegerField(null=True)
    apply_user_name = CharField(null=True)
    cancel_remark = CharField(null=True)
    cancel_time = DateTimeField(null=True)
    cancel_user_id = BigIntegerField(null=True)
    cancel_user_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    delivery_order_no = CharField(null=True)
    delivery_warehouse = CharField()
    freight = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    payment_id = BigIntegerField(index=True, null=True)
    payment_type = IntegerField()
    prepay_ratio = DecimalField(null=True)
    purchase_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    purchase_order_id = BigIntegerField(index=True)
    purchase_order_no = CharField(index=True)
    settlement_way = IntegerField()
    shipping_order_id = BigIntegerField(null=True)
    supplier_id = BigIntegerField()
    supplier_name = CharField()
    trace_id = CharField(null=True)
    tracer_id = BigIntegerField()
    tracer_name = CharField()
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_apply'


class SettlementApplyDetail(BaseModel):
    actual_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    all_apply_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    apply_exception_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    available_apply_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    delivery_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    exception_quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField()
    market_sku_img = CharField(null=True)
    market_sku_name_cn = CharField()
    market_sku_type = IntegerField()
    ratio = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    sale_attr_name_cn = CharField(null=True)
    settlement_apply_id = BigIntegerField(index=True)
    shipping_order_id = BigIntegerField(null=True)
    shipping_order_no = CharField(null=True)
    total_apply_amount = DecimalField()
    total_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    version = IntegerField(null=True)
    warehouse_store_number = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'settlement_apply_detail'


class SettlementApplyDetailSub(BaseModel):
    actual_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    all_apply_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    current_apply_amount = DecimalField()
    current_apply_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField()
    market_sku_img = CharField(null=True)
    market_sku_name_cn = CharField()
    market_sku_type = IntegerField()
    parent_detail_id = BigIntegerField()
    ratio = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    sale_attr_name_cn = CharField(null=True)
    shipping_order_id = BigIntegerField(null=True)
    shipping_order_no = CharField(null=True)
    sub_apply_exception_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    sub_apply_id = BigIntegerField(index=True)
    total_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    trace_id = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_apply_detail_sub'


class SettlementApplySub(BaseModel):
    apply_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    apply_time = DateTimeField(null=True)
    apply_type = IntegerField()
    apply_user_id = BigIntegerField(null=True)
    apply_user_name = CharField(null=True)
    cancel_remark = CharField(null=True)
    cancel_time = DateTimeField(null=True)
    cancel_user_id = BigIntegerField(null=True)
    cancel_user_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    delivery_order_no = CharField(null=True)
    delivery_warehouse = CharField()
    freight = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    parent_apply_id = BigIntegerField(index=True)
    parent_apply_no = CharField(index=True)
    payment_id = BigIntegerField(index=True, null=True)
    payment_no = CharField(index=True, null=True)
    payment_type = IntegerField()
    prepay_ratio = DecimalField(null=True)
    purchase_amount = DecimalField()
    purchase_order_id = BigIntegerField()
    purchase_order_no = CharField(index=True)
    remark = CharField(null=True)
    settlement_way = IntegerField()
    shipping_order_id = BigIntegerField(null=True)
    sub_apply_no = CharField(unique=True)
    sub_apply_status = IntegerField()
    supplier_id = BigIntegerField()
    supplier_name = CharField()
    trace_id = CharField(null=True)
    tracer_id = BigIntegerField()
    tracer_name = CharField()
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_apply_sub'


class SettlementException(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    exception_freight = DecimalField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_order_id = BigIntegerField()
    purchase_order_no = CharField(index=True)
    purchase_total_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    settlement_exception_no = CharField(index=True)
    settlement_exception_status = IntegerField()
    supplier_id = BigIntegerField()
    supplier_name = CharField()
    total_exception_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    trace_id = CharField(null=True)
    tracer_id = BigIntegerField()
    tracer_name = CharField()
    unprocessed_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_exception'


class SettlementExceptionDetail(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    exception_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    exception_quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField()
    market_sku_img = CharField(null=True)
    market_sku_name_cn = CharField(null=True)
    market_sku_type = IntegerField(null=True)
    payment_id = BigIntegerField(null=True)
    payment_no = CharField(null=True)
    sale_attr_name_cn = CharField(null=True)
    settlement_exception_id = BigIntegerField(index=True)
    settlement_exception_type = IntegerField()
    trace_id = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_exception_detail'


class SettlementExceptionFreight(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    exception_amount = DecimalField()
    freight_no = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    payment_id = BigIntegerField(null=True)
    payment_no = CharField(null=True)
    settlement_exception_id = BigIntegerField(index=True)
    trace_id = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_exception_freight'


class SettlementExceptionProcessLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    payment_id = BigIntegerField(index=True, null=True)
    payment_no = CharField(null=True)
    process_log_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    processed_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    settlement_exception_id = BigIntegerField(index=True)
    settlement_exception_no = CharField()
    trace_id = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_exception_process_log'


class SettlementFreight(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    freight_no = CharField(index=True)
    freight_status = IntegerField()
    freight_type = IntegerField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_order_id = BigIntegerField(null=True)
    purchase_order_no = CharField(index=True, null=True)
    supplier_id = BigIntegerField()
    supplier_name = CharField()
    total_amount = DecimalField()
    trace_id = CharField(null=True)
    tracer_id = BigIntegerField()
    tracer_name = CharField()
    unprocessed_amount = DecimalField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_freight'


class SettlementFreightProcessLog(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    freight_id = BigIntegerField(index=True)
    freight_log_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    freight_no = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    payment_id = BigIntegerField(null=True)
    payment_no = CharField(null=True)
    processed_amount = DecimalField()
    trace_id = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_freight_process_log'


class SettlementPayment(BaseModel):
    close_time = DateTimeField(null=True)
    closer_id = BigIntegerField(null=True)
    closer_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    delivery_warehouse = CharField()
    has_payment_exception = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    pay_time = DateTimeField(null=True)
    payer_id = BigIntegerField(null=True)
    payer_name = CharField(null=True)
    payment_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    payment_exception_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    payment_exception_status = IntegerField(null=True)
    payment_no = CharField(unique=True)
    payment_status = IntegerField()
    reject_remark = CharField(null=True)
    reject_time = DateTimeField(null=True)
    reject_user_id = BigIntegerField(null=True)
    reject_user_name = CharField(null=True)
    supplier_id = BigIntegerField()
    supplier_name = CharField()
    trace_id = CharField(null=True)
    tracer_id = BigIntegerField()
    tracer_name = CharField()
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_payment'


class SettlementPaymentDetail(BaseModel):
    actual_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    default_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField()
    market_sku_img = CharField(null=True)
    market_sku_name_cn = CharField(null=True)
    market_sku_type = IntegerField(null=True)
    parent_apply_no = CharField(null=True)
    payment_id = BigIntegerField(index=True)
    purchase_order_no = CharField(null=True)
    sale_attr_name_cn = CharField(null=True)
    shipping_order_no = CharField(null=True)
    sub_apply_no = CharField(null=True)
    total_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    total_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    trace_id = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_payment_detail'


class SettlementPaymentRemark(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    payment_id = BigIntegerField(index=True)
    remark = CharField(null=True)
    trace_id = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'settlement_payment_remark'


class ShippingOrder(BaseModel):
    arrived_status = IntegerField()
    cancel_remark = CharField(null=True)
    cancel_time = DateTimeField(null=True)
    cancel_user_id = BigIntegerField(null=True)
    cancel_user_name = CharField(null=True)
    complete_time = DateTimeField(null=True)
    complete_user_id = BigIntegerField(null=True)
    complete_user_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    delivery_warehouse = CharField()
    destination_warehouse = CharField()
    eccang_purchase_no = CharField(null=True)
    eccang_push_remark = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    entry_order_code = CharField(null=True)
    entry_order_id = IntegerField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    number = IntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_order_id = BigIntegerField(index=True)
    purchase_order_no = CharField()
    purchaser_id = BigIntegerField()
    purchaser_name = CharField()
    quality_test_type = IntegerField()
    shipping_order_no = CharField(unique=True)
    shipping_order_status = IntegerField()
    supplier_info_id = BigIntegerField()
    supplier_name = CharField()
    total_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    trace_id = CharField(null=True)
    tracer_id = BigIntegerField()
    tracer_name = CharField()
    version = IntegerField(null=True)

    class Meta:
        table_name = 'shipping_order'


class ShippingOrderLogisticsInfo(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    expect_arrive_time = DateField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    logistics_order_no = CharField(null=True)
    shipping_order_id = BigIntegerField(index=True)
    trace_id = CharField(null=True)
    transform_type = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'shipping_order_logistics_info'


class ShippingOrderReceiptLog(BaseModel):
    already_generated = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField()
    operate_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    operate_user_id = BigIntegerField()
    operate_user_name = CharField()
    order_number = CharField(null=True)
    shelves_order_code = CharField()
    shipping_order_no = CharField(index=True)
    trace_id = CharField(null=True)
    version = IntegerField(null=True)
    warehouse_store_number = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'shipping_order_receipt_log'


class ShippingOrderSkuInfo(BaseModel):
    amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    bom_detail = UnknownField(null=True)  # json
    bom_id = IntegerField(null=True)
    bom_version = CharField(null=True)
    cancel_number = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    cancel_remark = CharField(null=True)
    cancel_time = DateTimeField(null=True)
    cancel_user_id = BigIntegerField(null=True)
    cancel_user_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    delivery_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    exception_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    external_inventory = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    internal_inventory = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField(index=True, null=True)
    market_sku_img = CharField()
    market_sku_label = CharField(null=True)
    market_sku_name_cn = CharField()
    market_sku_type = IntegerField()
    order_no = CharField(null=True)
    origin_delivery_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    sale_attr_name_cn = CharField(null=True)
    shelves_time = DateTimeField(null=True)
    shipping_order_id = BigIntegerField(index=True)
    trace_id = CharField(null=True)
    version = IntegerField(null=True)
    warehouse_store_number = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'shipping_order_sku_info'


class ShortageDemand(BaseModel):
    cancel_time = DateTimeField(null=True)
    cancel_user_id = BigIntegerField(null=True)
    cancel_user_name = CharField(null=True)
    confirm_time = DateTimeField(null=True)
    confirm_user_id = BigIntegerField(null=True)
    confirm_user_name = CharField(null=True)
    create_time = DateTimeField(null=True)
    destination_warehouse = CharField(index=True, null=True)
    exception_remarks = CharField(null=True)
    exception_time = DateTimeField(null=True)
    exception_user_id = BigIntegerField(null=True)
    exception_user_name = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    sales_order_no = CharField(null=True)
    sales_order_remarks = CharField(null=True)
    shortage_demand_status = IntegerField(null=True)
    shortage_order_number = CharField(null=True)
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'shortage_demand'


class ShortageSkuInfo(BaseModel):
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField(index=True, null=True)
    market_sku_img = CharField(null=True)
    market_sku_label = IntegerField(null=True)
    market_sku_label_name = CharField(null=True)
    market_sku_name_cn = CharField(null=True)
    market_sku_type = IntegerField(null=True)
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    shortage_demand_id = BigIntegerField(null=True)
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'shortage_sku_info'
        indexes = (
            (('shortage_demand_id', 'is_deleted'), True),
        )


class SkuQuantityReport(BaseModel):
    create_time = DateTimeField()
    delivery_warehouse = CharField()
    demand_confirmed_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    demand_exception_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    demand_wait_confirm_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    destination_warehouse = CharField()
    id = BigAutoField()
    market_sku = CharField()
    order_arriving_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    order_audit_fail_quantity = IntegerField(null=True)
    order_draft_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    order_exception_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    order_wait_audit_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    order_wait_order_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    order_wait_shipping_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    plan_draft_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    plan_un_audit_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    plan_wait_audit_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sku_type = IntegerField(null=True)
    trace_id = CharField(null=True)

    class Meta:
        table_name = 'sku_quantity_report'


class SkuReceiptReport(BaseModel):
    actual_price = DecimalField()
    all_store_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    delivery_warehouse = CharField(index=True)
    destination_warehouse = CharField(index=True)
    entry_order_code = CharField(null=True)
    entry_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField()
    market_sku_name_cn = CharField()
    purchase_number = CharField(index=True)
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    ratio = DecimalField()
    receipt_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    shelves_order_code = CharField()
    shipping_order_no = CharField(index=True)
    supplier_info_id = BigIntegerField(index=True)
    supplier_name = CharField()
    total_amount = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    trace_id = CharField(null=True)
    version = IntegerField(null=True)
    warehouse_store_number = IntegerField(constraints=[SQL("DEFAULT 0")])

    class Meta:
        table_name = 'sku_receipt_report'


class StockPlan(BaseModel):
    cancel_remark = CharField(null=True)
    cancel_time = DateTimeField(null=True)
    cancel_user_id = BigIntegerField(null=True)
    cancel_user_name = CharField(null=True)
    confirm_remark = CharField(null=True)
    confirm_time = DateTimeField(null=True)
    confirm_user_id = BigIntegerField(null=True)
    confirm_user_name = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_user_name = CharField(null=True)
    delivery_warehouse = CharField(index=True, null=True)
    destination_warehouse = CharField(index=True, null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku_quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    purchase_remark = CharField(null=True)
    stock_plan_number = CharField(null=True)
    stock_plan_status = IntegerField(null=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'stock_plan'
        indexes = (
            (('stock_plan_number', 'is_deleted'), True),
        )


class StockSkuInfo(BaseModel):
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField(index=True, null=True)
    market_sku_img = CharField(null=True)
    market_sku_label_id = IntegerField(null=True)
    market_sku_name_cn = CharField(null=True)
    market_sku_type = IntegerField(null=True)
    min_purchase = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    quantity = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    remark = CharField(null=True)
    stock_plan_id = BigIntegerField(index=True, null=True)
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 1000")], null=True)

    class Meta:
        table_name = 'stock_sku_info'


class SupplierAttachment(BaseModel):
    attachment_name = CharField(null=True)
    attachment_type = CharField(null=True)
    attachment_url = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    supplier_id = BigIntegerField(index=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'supplier_attachment'


class SupplierCommunication(BaseModel):
    aliwangwang = CharField(null=True)
    contact = CharField(null=True)
    contact_address = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    phone_number = CharField(null=True)
    qq = CharField(null=True)
    return_address = CharField(null=True)
    return_postcode = CharField(null=True)
    supplier_id = BigIntegerField(index=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'supplier_communication'


class SupplierInfo(BaseModel):
    audit_date = IntegerField(null=True)
    check_remark = CharField(null=True)
    check_time = DateTimeField(null=True)
    check_user_id = BigIntegerField(null=True)
    check_user_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    developer_id = BigIntegerField()
    developer_name = CharField()
    drawback_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    eccang_push_remark = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    eccang_supplier_id = BigIntegerField(null=True)
    freight_bearer = IntegerField()
    id = BigAutoField()
    invoice_type = IntegerField(null=True)
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_need_quality = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_provide_invoice = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    is_use_supplier_portal = IntegerField(constraints=[SQL("DEFAULT 0")])
    main_category_id = CharField(null=True)
    main_category_name = CharField(null=True)
    management_type = IntegerField()
    packaging_me = IntegerField()
    payment_cycle = CharField(null=True)
    payment_date = IntegerField(null=True)
    payment_type = IntegerField()
    prepay_ratio = DecimalField(null=True)
    purchase_way = IntegerField()
    purchaser_id = BigIntegerField()
    purchaser_name = CharField()
    settlement_way = IntegerField()
    social_credit_code = CharField(null=True)
    stop_remark = CharField(null=True)
    supplier_code = CharField()
    supplier_level = CharField()
    supplier_name = CharField(index=True)
    supplier_password = CharField(null=True)
    supplier_status = IntegerField()
    supplier_type = CharField()
    supplier_user_name = CharField(null=True)
    taxpayer_type = IntegerField(null=True)
    trace_id = CharField(null=True)
    tracer_id = BigIntegerField()
    tracer_name = CharField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'supplier_info'
        indexes = (
            (('supplier_code', 'is_deleted'), True),
        )


class SupplierInfoOfficial(BaseModel):
    audit_date = IntegerField(null=True)
    check_remark = CharField(null=True)
    check_time = DateTimeField(null=True)
    check_user_id = BigIntegerField(null=True)
    check_user_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    creator_id = BigIntegerField(null=True)
    creator_name = CharField(null=True)
    developer_id = BigIntegerField(null=True)
    developer_name = CharField(null=True)
    drawback_type = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    eccang_push_remark = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    eccang_supplier_id = BigIntegerField(null=True)
    freight_bearer = IntegerField(null=True)
    id = BigAutoField()
    invoice_type = IntegerField(null=True)
    is_need_quality = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_provide_invoice = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    is_use_supplier_portal = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    main_category_id = CharField(null=True)
    main_category_name = CharField(null=True)
    management_type = IntegerField(null=True)
    packaging_me = IntegerField(null=True)
    payment_cycle = CharField(null=True)
    payment_date = IntegerField(null=True)
    payment_type = IntegerField(null=True)
    prepay_ratio = DecimalField(null=True)
    purchase_way = IntegerField(null=True)
    purchaser_id = BigIntegerField(null=True)
    purchaser_name = CharField(null=True)
    settlement_way = IntegerField(null=True)
    social_credit_code = CharField(null=True)
    stop_remark = CharField(null=True)
    supplier_code = CharField(null=True)
    supplier_level = CharField(null=True)
    supplier_name = CharField(null=True)
    supplier_password = CharField(null=True)
    supplier_status = IntegerField(null=True)
    supplier_type = CharField(null=True)
    supplier_user_name = CharField(null=True)
    taxpayer_type = IntegerField(null=True)
    trace_id = CharField(null=True)
    tracer_id = BigIntegerField(null=True)
    tracer_name = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'supplier_info_official'


class SupplierInventory(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    external_inventory = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    internal_inventory = IntegerField(constraints=[SQL("DEFAULT 0")])
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField()
    package_id = IntegerField()
    package_version = CharField()
    product_type_id = IntegerField()
    product_type_name = CharField()
    supplier_id = BigIntegerField(index=True)
    supplier_name = CharField()
    trace_id = CharField(null=True)
    uk = CharField(index=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'supplier_inventory'
        indexes = (
            (('market_sku', 'package_version'), False),
        )


class SupplierInventoryLog(BaseModel):
    id = BigAutoField()
    inventory_type = IntegerField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    number = IntegerField()
    operate_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    operate_type = IntegerField()
    operate_user_id = BigIntegerField()
    operate_user_name = CharField()
    remark = CharField(null=True)
    source_no = CharField(null=True)
    supplier_inventory_id = BigIntegerField(index=True)
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'supplier_inventory_log'


class SupplierPaymentMethod(BaseModel):
    account = CharField(null=True)
    account_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    id = BigAutoField()
    identity_card_no = CharField(null=True)
    is_default_account = IntegerField(null=True)
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    opening_bank = CharField(null=True)
    pay_way = CharField(null=True)
    receive_company = CharField(null=True)
    receiver = CharField(null=True)
    supplier_id = BigIntegerField(index=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'supplier_payment_method'


class SupplierPriceHistory(BaseModel):
    check_time = DateTimeField(null=True)
    check_user_id = BigIntegerField(null=True)
    check_user_name = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField()
    market_sku_id = BigIntegerField()
    purchase_price = CharField()
    supplier_id = BigIntegerField()
    supplier_product_id = BigIntegerField(index=True)
    tax_point = DecimalField()
    trace_id = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'supplier_price_history'


class SupplierProduct(BaseModel):
    check_remark = CharField(null=True)
    check_time = DateTimeField(null=True)
    check_user_id = BigIntegerField(null=True)
    check_user_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    eccang_push_remark = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    eccang_supplier_id = BigIntegerField(null=True)
    id = BigAutoField()
    is_default_supplier = IntegerField(constraints=[SQL("DEFAULT 1")])
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField(index=True)
    market_sku_id = BigIntegerField()
    minimum_number = IntegerField(constraints=[SQL("DEFAULT 0")])
    online_shopping_remark = CharField(null=True)
    online_shopping_url = CharField(null=True)
    package_detail = UnknownField(null=True)  # json
    package_id = IntegerField(null=True)
    package_version = CharField(null=True)
    product_name = CharField()
    product_tag_id = IntegerField(null=True)
    product_tag_name = CharField(null=True)
    product_type_id = IntegerField()
    product_type_name = CharField()
    purchase_delivery = IntegerField()
    supplier_id = BigIntegerField()
    supplier_item_no = CharField(null=True)
    supplier_product_status = IntegerField()
    tax_point = DecimalField()
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'supplier_product'
        indexes = (
            (('supplier_id', 'market_sku', 'is_deleted'), True),
        )


class SupplierProductOfficial(BaseModel):
    check_remark = CharField(null=True)
    check_time = DateTimeField(null=True)
    check_user_id = BigIntegerField(null=True)
    check_user_name = CharField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    creator_id = BigIntegerField(null=True)
    creator_name = CharField(null=True)
    eccang_push_remark = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    eccang_supplier_id = BigIntegerField(null=True)
    id = BigAutoField()
    is_default_supplier = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    market_sku = CharField(index=True, null=True)
    market_sku_id = BigIntegerField(null=True)
    minimum_number = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    online_shopping_remark = CharField(null=True)
    online_shopping_url = CharField(null=True)
    package_detail = UnknownField(null=True)  # json
    package_id = IntegerField(null=True)
    package_version = CharField(null=True)
    product_name = CharField(null=True)
    product_tag_id = IntegerField(null=True)
    product_tag_name = CharField(null=True)
    product_type_id = IntegerField(null=True)
    product_type_name = CharField(null=True)
    purchase_delivery = IntegerField(null=True)
    supplier_id = BigIntegerField(null=True)
    supplier_item_no = CharField(null=True)
    supplier_product_price = UnknownField(null=True)  # json
    supplier_product_status = IntegerField(null=True)
    tax_point = DecimalField(null=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'supplier_product_official'
        indexes = (
            (('supplier_id', 'market_sku'), True),
        )


class SupplierProductPrice(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    creator_id = BigIntegerField()
    creator_name = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")])
    market_sku = CharField()
    market_sku_id = BigIntegerField()
    minimum_order_quantity = IntegerField(constraints=[SQL("DEFAULT 0")])
    purchase_price = DecimalField(constraints=[SQL("DEFAULT 0.0000")])
    supplier_product_id = BigIntegerField(index=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField()
    update_user_name = CharField()
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'supplier_product_price'


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


class WarehouseRule(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField()
    create_user_name = CharField()
    delivery_warehouse_code = CharField()
    delivery_warehouse_name = CharField()
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    priority = IntegerField()
    remark = CharField(null=True)
    rule_name = CharField(unique=True)
    rule_status = IntegerField()
    trace_id = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'warehouse_rule'


class WarehouseRuleCondition(BaseModel):
    condition_group = IntegerField()
    condition_key = CharField()
    condition_type = IntegerField()
    condition_value = CharField()
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    create_user_id = BigIntegerField(null=True)
    create_user_name = CharField(null=True)
    id = BigAutoField()
    is_deleted = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    remark = CharField(null=True)
    rule_id = BigIntegerField(index=True)
    trace_id = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_user_name = CharField(null=True)
    version = IntegerField(null=True)

    class Meta:
        table_name = 'warehouse_rule_condition'
