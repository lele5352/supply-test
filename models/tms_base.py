from peewee import *
from config import tms_db_config

database = MySQLDatabase('supply_logistics_base', **tms_db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


class BaseDict(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    dict_type = CharField(index=True)
    dict_type_desc = CharField()
    id = BigAutoField()
    label_key = CharField(index=True)
    label_value = CharField()
    parent_key = CharField(null=True)
    remark = CharField(null=True)
    sort = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    use_type = IntegerField(constraints=[SQL("DEFAULT 2")])

    class Meta:
        table_name = 'base_dict'
        indexes = (
            (('label_key', 'dict_type', 'del_flag'), True),
        )


class BaseFeeItem(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    fee_item_category = IntegerField()
    fee_item_code = CharField()
    fee_item_name = CharField()
    fee_item_simple_name = CharField()
    fee_item_type = IntegerField()
    id = BigAutoField()
    remark = CharField(null=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'base_fee_item'
        indexes = (
            (('fee_item_code', 'del_flag'), True),
        )


class BaseFeeItemMapping(BaseModel):
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    fee_item_id = BigIntegerField()
    id = BigAutoField()
    mapping_code = CharField()
    mapping_formula = CharField(null=True)
    mapping_name = CharField(null=True)
    mapping_type = IntegerField(null=True)
    mapping_value = CharField()
    remark = CharField(null=True)
    sort = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'base_fee_item_mapping'
        indexes = (
            (('fee_item_id', 'del_flag'), False),
        )


class BaseRegion(BaseModel):
    country_id = BigIntegerField(null=True)
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    latitude = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    longitude = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    parent_id = BigIntegerField(null=True)
    path_code = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    path_name = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    region_code = CharField(constraints=[SQL("DEFAULT ''")])
    region_name_cn = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    region_name_en = CharField(constraints=[SQL("DEFAULT ''")], null=True)
    type = IntegerField()
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)
    zip_code = CharField(constraints=[SQL("DEFAULT ''")])
    zone_id = CharField(constraints=[SQL("DEFAULT ''")], null=True)

    class Meta:
        table_name = 'base_region'
        indexes = (
            (('country_id', 'type', 'del_flag'), False),
            (('type', 'parent_id', 'region_code'), True),
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
