# 自定义业务异常类

class MissingPasswordError(Exception):
    def __init__(self):
        self.message = "Password is required when username is provided"
        super().__init__(self.message)


class FileImportError(Exception):
    def __init__(self, filename):
        self.message = f"文件 {filename} 上传失败，未获取到url"
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
