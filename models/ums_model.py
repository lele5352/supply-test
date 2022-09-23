from peewee import *

from config import db_config

database = MySQLDatabase('supply_auth', **db_config)


class UnknownField(object):
    def __init__(self, *_, **__): pass


class BaseModel(Model):
    class Meta:
        database = database


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


class OauthClientDetails(BaseModel):
    access_token_validity = IntegerField(null=True)
    additional_information = CharField(null=True)
    authorities = CharField(null=True)
    authorized_grant_types = CharField(null=True)
    autoapprove = CharField(null=True)
    client_id = CharField(unique=True)
    client_secret = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    refresh_token_validity = IntegerField(null=True)
    resource_ids = CharField(null=True)
    scope = CharField(null=True)
    web_server_redirect_uri = CharField(null=True)

    class Meta:
        table_name = 'oauth_client_details'


class SysDataRole(BaseModel):
    code = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user_id = BigIntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    name = CharField(null=True)
    remark = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user_id = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'sys_data_role'


class SysDept(BaseModel):
    create_time = DateTimeField(null=True)
    create_user = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    level = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    name = CharField(null=True)
    parent_id = BigIntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sort = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user = BigIntegerField(null=True)

    class Meta:
        table_name = 'sys_dept'


class SysDeptRole(BaseModel):
    create_time = DateTimeField(null=True)
    create_user = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    dept_id = BigIntegerField(null=True)
    id = BigAutoField()
    role_id = BigIntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user = BigIntegerField(null=True)

    class Meta:
        table_name = 'sys_dept_role'


class SysResource(BaseModel):
    component = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    icon = CharField(null=True)
    id = BigAutoField()
    keep_alive = IntegerField(null=True)
    parent_id = BigIntegerField(null=True)
    path = CharField(null=True)
    permission = CharField(null=True)
    resource_code = CharField(constraints=[SQL("DEFAULT ''")])
    resource_name = CharField(null=True)
    sort = IntegerField(constraints=[SQL("DEFAULT 1")], null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    sys_type = IntegerField(constraints=[SQL("DEFAULT 1")])
    type = IntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user = BigIntegerField(null=True)

    class Meta:
        table_name = 'sys_resource'


class SysResourceUrl(BaseModel):
    create_time = DateTimeField(null=True)
    create_user = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    operate_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    req_method = CharField(constraints=[SQL("DEFAULT 'POST'")], null=True)
    resource_id = BigIntegerField(constraints=[SQL("DEFAULT 1")], index=True)
    update_time = DateTimeField(null=True)
    update_user = BigIntegerField(null=True)
    url = CharField(null=True)
    url_name = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'sys_resource_url'


class SysResourceUrlBkp(BaseModel):
    create_time = DateTimeField(null=True)
    create_user = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    operate_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    req_method = CharField(constraints=[SQL("DEFAULT 'POST'")], null=True)
    resource_id = BigIntegerField(constraints=[SQL("DEFAULT 1")])
    update_time = DateTimeField(null=True)
    update_user = BigIntegerField(null=True)
    url = CharField(null=True)
    url_name = CharField(constraints=[SQL("DEFAULT ''")])

    class Meta:
        table_name = 'sys_resource_url_bkp'


class SysRole(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField()
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    operate_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    role_code = CharField()
    role_desc = CharField(null=True)
    role_name = CharField()
    role_type = IntegerField(constraints=[SQL("DEFAULT 0")])
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = BigIntegerField(null=True)
    update_username = CharField(null=True)

    class Meta:
        table_name = 'sys_role'


class SysRoleDataPerm(BaseModel):
    biz_type = CharField(null=True)
    create_time = DateTimeField(null=True)
    create_user = BigIntegerField(null=True)
    data_id = BigIntegerField(null=True)
    default_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    remark = CharField(null=True)
    role_id = BigIntegerField(null=True)
    sys_type = CharField(null=True)
    update_time = DateTimeField(null=True)
    update_user = BigIntegerField(null=True)

    class Meta:
        table_name = 'sys_role_data_perm'


class SysRoleResource(BaseModel):
    create_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    create_user = BigIntegerField()
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")])
    id = BigAutoField()
    resource_id = BigIntegerField(index=True)
    role_id = BigIntegerField(index=True)
    update_time = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")], null=True)
    update_user = BigIntegerField(null=True)

    class Meta:
        table_name = 'sys_role_resource'


class SysUser(BaseModel):
    create_time = DateTimeField(null=True)
    create_user = IntegerField(null=True)
    create_username = CharField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    email = CharField(null=True)
    id = BigAutoField()
    mobile = CharField(null=True)
    nickname = CharField(null=True)
    password = CharField(null=True)
    state = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    update_time = DateTimeField(null=True)
    update_user = IntegerField(null=True)
    update_username = CharField(null=True)
    username = CharField(index=True)
    version = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)

    class Meta:
        table_name = 'sys_user'


class SysUserAuth(BaseModel):
    id = BigAutoField()
    open_id = CharField(null=True)
    type = IntegerField(null=True)
    user_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'sys_user_auth'


class SysUserDataRole(BaseModel):
    create_time = DateTimeField(null=True)
    create_user = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    role_id = BigIntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user = BigIntegerField(null=True)
    user_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'sys_user_data_role'


class SysUserDept(BaseModel):
    create_time = DateTimeField(null=True)
    create_user = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    dept_id = BigIntegerField(null=True)
    id = BigAutoField()
    update_time = DateTimeField(null=True)
    update_user = BigIntegerField(null=True)
    user_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'sys_user_dept'


class SysUserRole(BaseModel):
    create_time = DateTimeField(null=True)
    create_user = BigIntegerField(null=True)
    del_flag = IntegerField(constraints=[SQL("DEFAULT 0")], null=True)
    id = BigAutoField()
    role_id = BigIntegerField(null=True)
    update_time = DateTimeField(null=True)
    update_user = BigIntegerField(null=True)
    user_id = BigIntegerField(null=True)

    class Meta:
        table_name = 'sys_user_role'
