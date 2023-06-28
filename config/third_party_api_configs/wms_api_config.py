from config.third_party_api_configs import ApiConfig


class BaseApiConfig:
    class GetWarehouseInfo(ApiConfig):
        uri_path = "/warehouse/bycode/"
        method = "GET"

    class GetWarehouseInfoById(ApiConfig):
        uri_path = "ec-wms-api/warehouse/"
        method = "GET"

    class GetSwitchWarehouseList(ApiConfig):
        uri_path = "/api/ec-wms-api/data/permission/user/list"
        method = "GET"
        data = {"t": 1640053950389}

    class SwitchDefaultWarehouse(ApiConfig):
        uri_path = "/api/ec-wms-api/data/permission/switchdefault"
        method = "PUT"
        data = {"dataPermId": 854}

    class CreateLocation(ApiConfig):
        uri_path = "/api/ec-wms-api/location/save"
        method = "POST"
        data = {
            "belongWarehouseId": 19,  # 所属仓库
            "belongWarehouseAreaId": 15,  # 所属库区
            "warehouseAreaType": 1,  # 库区类型 0-上架区 1-不良品区 2-入库异常处理区 3-出库异常处理区 4-出库异常处理区 5-容器库区
            "warehouseLocationCode": "KWBM",  # 库位编码
            "warehouseLocationName": "KW",  # 库位名称
            "destWarehouseId": 7,  # 目的仓id
            "warehouseLocationType": 1,  # 库位类型 1-收货库位 2-质检库位 3-调拨库位 4-移库库位 5-上架库位 6-不良品库位 7-入库异常库位 8-出库异常库位}
            "warehouseLocationUseStatus": 0,
            "inventoryDistributeLevel": 2
        }

    class WorkdayDuration(ApiConfig):
        """获取节假日时长"""
        uri_path = '/warehouse/workday/duration'
        method = 'POST'
        data = {
            "warehouseId": None,
            "startTime": "",  # 北京时间，格式 yyyy-MM-dd HH:mm:ss
            "endTime": ""  # 北京时间，格式 yyyy-MM-dd HH:mm:ss
        }

    class WorkdayTargetDateTime(ApiConfig):
        """根据时长和工作日数据查询目标时间"""
        uri_path = '/warehouse/workday/targetDateTime'
        method = 'POST'
        data = {
            "warehouseId": None,
            "dateTime": "",  # 北京时间，格式 yyyy-MM-dd HH:mm:ss
            "duration": ""  # 时长，如 60h,30m,1d,1s"
        }


class OtherInApiConfig:
    class GetSkuInfo(ApiConfig):
        uri_path = "/api/ec-wms-api/entryorder/addSkuInfoPage"
        method = "POST"
        data = {"skuCode": None, "skuCodeLike": None, "skuName": None, "saleSkuCode": None, "saleSkuCodeLike": None,
                "size": 10, "current": 1}

    class CreateOtherInOrder(ApiConfig):
        uri_path = "/api/ec-wms-api/entryorder"
        method = "POST"
        data = {"entryOrderType": 3, "eta": 1669873281000, "supplierCode": None, "fromOrderCode": None, "remark": None,
                "qualityType": 0, "timestamp": 1669873281000, "logisticsInfoList": [], "skuInfoList": [
                {"warehouseSkuCode": "JFO91L3917A01", "planSkuQty": 1, "warehouseSkuName": "包装方案名称1 1/1 X1",
                 "warehouseSkuWeight": 4.11, "saleSkuCode": "JFO91L3917",
                 "saleSkuName": "LI-计划系统测试商品-可/不可跨仓", "bomVersion": "A",
                 "saleSkuImg": "https://img.popicorns.com/mall/file/2021/10/19/3109bcabaf6a46c5ae191d7e44246c62.jpeg",
                 "warehouseSkuHeight": 3.1, "warehouseSkuLength": 1.1, "warehouseSkuWidth": 2.1}], "operationFlag": 0}

    class SubmitOtherInOrder(ApiConfig):
        uri_path = "/api/ec-wms-api/entryorder"
        method = "PUT"
        data = {"entryOrderId": "85846", "entryOrderType": 3, "eta": 1669824000000, "supplierCode": None,
                "fromOrderCode": None, "qualityType": 0, "remark": None, "logisticsInfoList": [], "skuInfoList": [
                {"warehouseSkuCode": "JFO91L3917A01", "planSkuQty": 2, "warehouseSkuName": "包装方案名称1",
                 "warehouseSkuWeight": 4.11, "saleSkuCode": "JFO91L3917",
                 "saleSkuName": "LI-计划系统测试商品-可/不可跨仓", "bomVersion": "A",
                 "saleSkuImg": "https://img1.popicorns.com/fit-in/200x200/mall/file/2021/10/19/3109bcabaf6a46c5ae191d7e44246c62.jpeg",
                 "warehouseSkuHeight": 3.1, "warehouseSkuLength": 1.1, "warehouseSkuWidth": 2.1}], "operationFlag": 1}

    class GetOtherInOrderSkuInfoByEntryOrderCode(ApiConfig):
        uri_path = "/api/ec-wms-api/entryorder/getSkuInfoByEntryCode"
        method = "POST"
        data = {"size": 100, "current": 1, "entryOrderCode": "RK2212010004", "entryOrderId": "85848"}

    class PutOnTheShelf(ApiConfig):
        uri_path = "/api/ec-wms-api/entryorder/putOnTheShelf"
        method = "POST"
        data = {"entryOrderId": 85847, "skuList": [
            {"skuCode": "JFO91L3917A01", "shelvesLocationCode": "NJ01-A01-101", "skuQty": "1", "abnormalQty": 0}]}


class TransferApiConfig:
    class CreateTransferDemand(ApiConfig):
        uri_path = "/transferDemand/create"
        method = "POST"
        data = {
            "receiveWarehouseCode": "LA01",
            "receiveTargetWarehouseCode": "",
            "deliveryWarehouseCode": "FSBH",
            "deliveryTargetWarehouseCode": "",
            "userId": 1,
            "username": "admin",
            "goodsSkuCode": "53586714577",
            "bomVersion": "A",
            "demandQty": 5,
            "customerType": 1,  # 1：普通客户 2 ：大客户
            "customerRemark": "客戶備注",
            "sourceCode": "aaaaaaaaaaaaaaa",
            "demandType": 1  # 1:按需调拨需求 2：备货调拨需求
        }

    class CreateTransferPickOrder(ApiConfig):
        uri_path = "/api/ec-wms-api/transferOut/picking/create"
        method = "POST"
        data = {"demandCodes": ["XQ2201250017"], "pickType": 1}

    class TransferPickOrderAssign(ApiConfig):
        uri_path = "/api/ec-wms-api/transferOut/picking/assignPickUser"
        method = "POST"
        data = {"pickOrderNos": ["DJH2201250008"], "pickUsername": "李强", "pickUserId": "3"}

    class TransferConfirmPick(ApiConfig):
        uri_path = "/api/ec-wms-api/transferOut/picking/doPicking"
        method = "POST"
        data = {"pickOrderNo": ["DJH2201250008"], "details": []}

    class TransferPickOrderDetail(ApiConfig):
        uri_path = "/api/ec-wms-api/transferOut/picking/detail/%s"
        method = "GET"
        data = {"t": 1643333857384}

    class TransferSubmitTray(ApiConfig):
        uri_path = "/api/ec-wms-api/transferOut/pda/submitTrayInfo"
        method = "POST"
        data = [{
            "storageLocationCode": "TPKW-001",
            "pickOrderNo": "DJH2201290004",
            "trayInfos": [{
                "id": 792,
                "waresSkuCode": "63203684930A02",
                "waresSkuName": "酒柜(金色)07 2/2 X5",
                "goodsSkuCode": "63203684930",
                "goodsSkuName": "棕色木纹四裙垂直边独立式浴缸3",
                "skuQty": 10
            }]}]

    class TransferPickOrderTrayDetail(ApiConfig):
        uri_path = "/api/ec-wms-api/transferOut/tray/detail?pickOrderNo=%s"
        method = "GET"
        data = ""

    class TransferFinishPacking(ApiConfig):
        uri_path = "/api/ec-wms-api/transferOut/pda/finishPacking"
        method = "POST"
        data = {
            "pickOrderNo": "",
            "storageLocationCodes": []
        }

    class TransferOutOrderDetail(ApiConfig):
        uri_path = "/api/ec-wms-api/transferOut/handover/boxes?transferOutNo=%s"
        method = "GET"

    class TransferOutOrderReview(ApiConfig):
        uri_path = "/api/ec-wms-api/transferOut/box/review/submit"
        method = "POST"
        data = {
            "boxNo": "DC2202070002-1",
            "storageLocationCode": "TPKW-001"
        }

    class TransferBoxBind(ApiConfig):
        uri_path = "/api/ec-wms-api/transferOut/handover/bind"
        method = "POST"
        data = {
            "boxNo": "DC2202070002-1",
            "handoverNo": "",
            "receiveWarehouseCode": ""
        }

    class TransferDelivery(ApiConfig):
        uri_path = "/api/ec-wms-api/transferOut/handover/delivery/confirm"
        method = "POST"
        data = {"handoverNo": ""}

    class TransferInReceived(ApiConfig):
        uri_path = "/api/ec-wms-api/transferIn/handover/received/confirm"
        method = "POST"
        data = {"handoverNo": ""}

    class TransferBoxUpShelf(ApiConfig):
        uri_path = "/api/ec-wms-api/transferIn/input/box/shelf"
        method = "POST"
        data = {
            "boxNo": "DC2202070021-1",
            "storageLocationCode": "SJKW-001"
        }


class OtherEntryOrderApiConfig:
    class CreateOtherEntryOrder(ApiConfig):
        uri_path = "/api/ec-wms-api/entryorder"
        method = "PUT"
        data = {
            "receiveWarehouseCode": "LA01",
            "deliveryWarehouseCode": "FSBH",
            "userId": 1,
            "username": "admin",
            "goodsSkuCode": "53586714577",
            "demandQty": 5,
            "customerType": 1,  # 1：普通客户 2 ：大客户
            "customerRemark": "客戶備注",
            "sourceCode": "aaaaaaaaaaaaaaa",
            "demandType": 1  # 1:按需调拨需求 2：备货调拨需求
        }


class DeliveryApiConfig:
    class DeliveryOrderPage(ApiConfig):
        uri_path = "/api/ec-wms-api/delivery-order/page"
        method = "POST"
        data = {"deliveryOrderCodeList": ["PRE-CK2211100010"], "saleOrderCodeList": None, "packageCodeList": None,
                "expressOrderCodeList": None, "skuCodeList": None, "saleSkuCodeList": None, "stateList": [],
                "prodType": None, "expressOrderState": None, "packageState": None, "hasPackage": None,
                "transportMode": None, "operationMode": None, "interceptFlag": "", "cancelFlag": "", "priority": None,
                "logisticsCodeList": None, "channelCodeList": None, "planLogisticsCodeList": None,
                "planChannelCodeList": None, "platform": None, "store": None, "customerType": None, "hasTickets": None,
                "countryCode": None, "createTimeStart": None, "createTimeEnd": None, "pickOrderCodes": None,
                "expressChangeFlag": None, "saleOrderTypes": None, "props": [], "size": 10, "current": 1}

    class DeliveryOrderDetail(ApiConfig):
        uri_path = "/api/ec-wms-api/delivery-order/info/{0}"
        method = "GET"
        data = {"t": 1668051101602}

    class AssignStock(ApiConfig):
        uri_path = "/api/ec-wms-api/delivery-order/stock-assign/v2"
        method = "POST"
        data = {"deliveryOrderCodes": ["PRE-CK2211060001"]}

    class PackageCallBack(ApiConfig):
        uri_path = "/api/ec-wms-api/delivery-order-api/push-plan"
        method = "POST"
        data = {
            "deliveryNo": "PRE-CK2211090021",
            "status": 1,
            "transportType": 2,
            "packageInfo": {
                "channelPrice": "123",
                "packageCount": 1,
                "packageIds": ["2"],
                "packageList": [
                    {
                        "packageNo": "PRE-CK2211090021",
                        "channelPrice": "1000",
                        "channelId": "181",
                        "channelCode": "unknow",
                        "channelName": "unknow快递",
                        "serviceId": "36",
                        "serviceCode": "unknow",
                        "serviceName": "unknow",
                        "timeValue": "1",
                        "length": "112",
                        "width": "113",
                        "height": "113",
                        "weight": "55",
                        "packageSkuList": [
                            {
                                "skuCode": "JJH3C94287A01",
                                "skuName": "包装名称1 1/2 X1",
                                "num": 3
                            },
                            {
                                "skuCode": "JJH3C94287A02",
                                "skuName": "包装名称2 2/2 X1",
                                "num": 3
                            }
                        ]
                    }
                ]
            },
            "code": 1,
            "info": "success"
        }

    class LabelCallBack(ApiConfig):
        uri_path = "/api/ec-wms-api/delivery-order-api/push-express-order/v2"
        method = "POST"
        data = {
            "deliveryNo": "PRE-CK2205050011",
            "orderList": [
                {
                    "expressChangeFlag": 0,
                    "expressChangeVersion": "1",
                    "deliveryNo": "PRE-CK2205050011",
                    "packageNoList": [
                        "PRE-BG2205050039"
                    ],
                    "logistyNo": "64324234152-119900",
                    "barCode": "534574353214234-119900",
                    "serviceName": "正式-Postpony",
                    "serviceCode": "prod-PostPony",
                    "channelName": "正式-PostPony-PostPony",
                    "channelCode": "UspsFirstClassMail",
                    "fileList": [
                        {
                            "filePath": "https://img.popicorns.com/dev/file/2022/02/28/f8a138a6a3e5447cad33a9ab9cc800fa.pdf",
                            "fileType": "pdf",
                            "fileCategory": "1",
                            "fileScale": "10*10",
                            "fileCopies": "1",
                            "filePrintDirection": "0"
                        }
                    ],
                    "extInfo": "{\"logisticsMerchant\": \"UPS1\", \"turnOrderNo\": \"转运单号123123\"}",
                    "turnOrderNo": "543255",
                    "drawOrderNo": "7879096854"
                }
            ]
        }

    class CreatePickOrder(ApiConfig):
        uri_path = "/api/ec-wms-api/delivery-order/create-pick-order"
        method = "PUT"
        data = {"singleDeliveryOrderCodes": ["PRE-CK2211130002"], "singleMaxQty": 1, "singlePickType": 0,
                "multiDeliveryOrderCodes": [], "multiPickType": 0}

    class AssignPickUser(ApiConfig):
        uri_path = "/api/ec-wms-api/pick-order/set-pick-user"
        method = "POST"
        data = {"pickOrderCodeList": ["XJH2211130002"], "userId": 418, "userName": "许宏伟"}

    class GetToPickData(ApiConfig):
        uri_path = "/api/ec-wms-api/pick-order/to-pick/%s"
        method = "GET"
        data = {"t": 0}

    class PickOrderConfirmPick(ApiConfig):
        uri_path = "/api/ec-wms-api/pick-order/save-pick-result"
        method = "PUT"
        data = {
            "pickOrderCode": "XJH2211130005",
            "normalList": [{"deliveryOrderCode": "PRE-CK2211130006", "skuCode": "67330337129A01",
                            "expressOrderCode": "logistyNo1668315676240", "skuQty": 24, "locationCode": "GZZF-SJKW99"}],
            "errList": []}

    class DeliverySavePackage(ApiConfig):
        uri_path = "/api/ec-wms-api/delivery-order/save-package"
        method = "POST"
        data = {
            "deliveryOrderCode": "PRE-CK2211130021",
            "packageInfoList": [
                {"packageIndex": 0,
                 "remarks": "{\"logistics_code\":\"unknow\",\"logistics_name\":\"unknow\",\"channel_code\":\"unknow\",\"channel_name\":\"unknow快递\"}",
                 "length": 44.1, "width": 44.5,
                 "height": 44.5, "weight": 121.254,
                 "skuInfoList": [
                     {"skuCode": "63203684930A01",
                      "skuQty": 2},
                     {"skuCode": "63203684930A02",
                      "skuQty": 10}]}],
            "transportType": 2,
            "expressOrderFlag": 1
        }

    class DeliveryPackageInfo(ApiConfig):
        uri_path = "/api/ec-wms-api/delivery-order/package-info/%s"
        method = "GET"
        data = {"t": 0}

    class DeliveryOrderReview(ApiConfig):
        uri_path = "/api/ec-wms-api/delivery-order/re-confirm"
        method = "POST"
        data = {"unNormalList": [], "normalList": []}

    class DeliveryOrderShipping(ApiConfig):
        uri_path = "/api/ec-wms-api/delivery-order/shipping"
        method = "POST"
        data = {"normalIdList": [15025], "normalCodeList": ["PRE-CK2211130010"], "unNormalList": []}


class ReceiptApiConfig:
    class EntryOrderPage(ApiConfig):
        uri_path = "/api/ec-wms-api/entryorder/page"
        method = "POST"
        data = {"sortField": [{"field": "create_time", "type": "DESC"}], "entryOrderCode": None,
                "entryOrderType": None,
                "entryOrderState": None, "likeLogisticsCompanyName": None, "warehouseSkuCodeList": None,
                "saleSkuCodeList": None, "shipmentNumberList": None, "purchaseOrderCode": None,
                "destWarehouseId": None,
                "qualityType": None, "supplierCode": None, "distributeOrderCodeList": ["FH2210215796"], "size": 10,
                "current": 1}

    class EntryOrderDetail(ApiConfig):
        uri_path = "/api/ec-wms-api/receivegoods/order/detail?entryOrderCode=%s"
        method = "GET"

    class PreReceiveOrder(ApiConfig):
        uri_path = "/api/ec-wms-api/receivegoods/save/preReceiptOrder"
        method = "POST"
        data = {
            "entryOrderCode": "RK2210210001",
            "predictReceiptOrderCode": "YSH2210240001",
            "skuList": [{
                "locationCode": "SHKW-005",
                "skuCode": "63203684930C01",
                "skuNumber": 1,
                "length": 0,
                "width": 0,
                "height": 0,
                "weight": 0
            }]
        }

    class SubmitPreReceiveOrder(ApiConfig):
        uri_path = "/api/ec-wms-api/receivegoods/submit/preReceiptOrder"
        method = "POST"
        data = {"predictReceiptOrderCodeList": []}

    class HandoverToQualityCheck(ApiConfig):
        uri_path = "/api/ec-wms-api/receivegoodshandover/confirm"
        method = "POST"
        data = {
            "locationCodes": ["SH1667739868494", "SH1667739868078"],
            "qualityType": 1
        }

    class QualityCheckLocationDetail(ApiConfig):
        uri_path = "/api/ec-wms-api/qualitycheck/location/detail"
        method = "GET"
        data = {"locationCode": ""}

    class QualityCheckLocationBind(ApiConfig):
        uri_path = "/api/ec-wms-api/qualitycheck/qc/location"
        method = "POST"
        data = {
            "receiveLocationCode": "SH1667739868494",
            "qcLocationCode": "ZJKW-001",
            "receiveOrderCode": "SH2303030002"
        }

    class QualityCheckSubmit(ApiConfig):
        uri_path = "/api/ec-wms-api/qualitycheck/save"
        method = "POST"
        data = {
            "skuList": [{
                "receiveLocationCode": "SH1667739868078",
                "entryOrderCode": "RK2303030011",
                "receiveOrderCode": "SH2303030002",
                "skuCode": "63203684930B01",
                "qcResult": 0,
                "number": 1,
                "length": 0,
                "height": 0,
                "width": 0,
                "weight": 0,
                "qcLocationCode": "ZJKW-001"
            }]
        }

    class HandoverToUpShelf(ApiConfig):
        uri_path = "/api/ec-wms-api/receivegoodshandover/confirmUpShelf"
        method = "POST"
        data = {"locationCodes": ["ZJKW-001"]}

    class UpShelfWholeLocation(ApiConfig):
        uri_path = "/api/ec-wms-api/upshelfV2/location/entireUpshelf"
        method = "POST"
        data = {"upshelfLocationCode": "KW-SJQ-01", "oldLocationCode": "TX-ZJ001"}

    class CompleteUpShelf(ApiConfig):
        uri_path = "/api/ec-wms-api/upshelfV2/location/confirmUpshelf"
        method = "POST"

    class LocationDetail(ApiConfig):
        uri_path = "/api/ec-wms-api/upshelfV2/location/detail?locationCodes=%s"
        method = "POST"


class StockOperationApiConfig:
    """库内作业相关"""
    class InventoryProcessOrderCreate(ApiConfig):
        """新增盘点单"""
        uri_path = '/api/ec-wms-api/inventoryProcessOrder/create'
        method = 'POST'
        data = {
            "inventoryProcessLatitude": 0,  # 盘点类型(0-常规盘点;1-短拣盘点;2-抽盘)
            "inventoryProcessRange": 0,     # 盘点维度(0-库位;1-SKU)
            "inventoryProcessType": 0,      # 盘点范围(0-库位;1-库存+SKU)
            "locDetails": [                 # 盘点单库位详情(盘点纬度是库位时，不能为空)--非必须
                {
                    "locCode": "KW-SJQ-3150"
                }
            ],
            "skuDetails": [                  # 盘点单SKU详情(盘点纬度是SKU时，不能为空)--非必须
                {
                    "locCode": "ut est incididunt aute deserunt",
                    "skuCode": "elit deserunt cupidatat laboris"
                },
                {
                    "locCode": "enim",
                    "skuCode": "in"
                }
            ]
        }

    class InventoryProcessOrderGenerateTask(ApiConfig):
        """盘点单生成盘点任务"""
        uri_path = '/api/ec-wms-api/inventoryProcessOrder/generateTask'
        method = 'POST'
        data = {
                "inventoryProcessOrderNo": "PD2301310012",  #盘点单号
                "operationMode": 1,     #作业类型(0-PDA盘点;1-纸质单盘点)
                "maxQty": 1     #每个任务最大数量
        }

    class InventoryProcessAssign(ApiConfig):
        """盘点任务分配操作人员"""
        uri_path = '/api/ec-wms-api/inventoryProcessTask/assign'
        method = 'POST'
        data = {
                "inventoryProcessTaskNo": [     #盘点任务号，支持批量
                    "PD2301310003_T1-1"
                ],
                "inventoryProcessUserId": 308,      #盘点人ID
                "inventoryProcessUsername": "黄乐乐",      #盘点人名称
                "source": 1
        }

    class InventoryProcessPrint(ApiConfig):
        """盘点任务打印，触发库存快照生成，以便继续操作盘点任务单据"""
        uri_path = '/api/ec-wms-api/inventoryProcessTask/print?'
        method = 'GET'
        data = {
                "inventoryProcessTaskNo": "PD2301310003_T1",    #盘点任务单号
                "t": 1675135653934      #当前时间戳
        }

    class InventoryProcessPrintTimes(ApiConfig):
        """打印次数"""
        uri_path = '/api/ec-wms-api/inventoryProcessTask/printTimes?'
        method = 'GET'
        data = {
            "inventoryProcessTaskNo": "PD2301310003_T1",  # 盘点任务单号
            "t": 1675135653934  # 当前时间戳
        }

    class InventoryProcessTaskDetailPage(ApiConfig):
        """获取盘点任务单详情页"""
        uri_path = '/api/ec-wms-api/inventoryProcessTask/detailPage'
        method = 'POST'
        data = {
            "inventoryProcessTaskId": "1905",   #盘点任务单id
            "size": 10000,
            "current": 1
        }

    class InventoryProcessCommit(ApiConfig):
        """盘点任务录入--提交"""
        uri_path = '/api/ec-wms-api/inventoryProcessTask/detailPage'
        method = 'POST'
        data = {
            "inventoryProcessTaskNo": "PD2301160033_T1-1",      #盘点任务单号
            "commitDetails": [{     #盘点明细
                "skuCode": "28265130025A01",
                "locCode": "KW-SJQ-3000",
                "inventoryProcessTaskNo": "PD2301160033_T1-1",
                "inventoryProcessTaskDetailId": 4609,
                "inventoryProcessQty": 3,       #盘点实际数量
                "inventoryStartQty": 3      #盘点开始数量
            }, {
                "skuCode": "J020053-11A01",
                "locCode": "KW-SJQ-3000",
                "inventoryProcessTaskNo": "PD2301160033_T1-1",
                "inventoryProcessTaskDetailId": 4610,
                "inventoryProcessQty": 7,
                "inventoryStartQty": 7
            }]
        }