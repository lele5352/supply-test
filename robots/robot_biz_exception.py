# 自定义业务异常类

class MissingPasswordError(Exception):
    def __init__(self):
        self.message = "Password is required when username is provided"
        super().__init__(self.message)


class FileImportError(Exception):
    def __init__(self, filename):
        self.message = f"文件 {filename} 上传失败，未获取到url"
        super().__init__(self.message)


class InventoryNotEnough(Exception):
    def __init__(self, sku, bom, warehouse_id):
        self.message = f"仓库id= {warehouse_id}, sku编码 {sku} , BOM版本 {bom} 库存不足"
        super().__init__(self.message)


class PlatSkuValueError(Exception):
    def __init__(self, sku):
        self.message = f"{sku} 缺少必需字段，请检查平台sku详情以下字段是否有值：platformCode，storeCode，fnSkuCode"
        super().__init__(self.message)


class PlatSkuNotFoundError(Exception):
    def __init__(self, sku):
        self.message = f"销售sku: {sku} 查询不到对应的平台sku，请先往【基础商品-商品信息-平台sku】进行添加"
        super().__init__(self.message)


class PlatTransferDemandSaveError(Exception):
    def __init__(self, file_url):
        self.message = f"平台调拨需求导入失败，请下载失败文件查看-> {file_url}"
        super().__init__(self.message)


class ConfigImportError(Exception):
    def __init__(self, config_name):

        error_message = {
            "rds": "请先在config __init__.py中添加配置：rds_config = env_config.redis_config.get(env)"
        }
        self.message = error_message.get(config_name, "import error")
        super().__init__(self.message)


class ConfigNotFoundError(Exception):

    def __init__(self, config_name, proj_name):
        error_message = {
            "rds": f"未找到项目 {proj_name} 的redis配置，请先在env_config.py中添加"
        }
        self.message = error_message.get(config_name, "import error")
        super().__init__(self.message)
