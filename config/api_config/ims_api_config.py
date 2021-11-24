ims_api_config = {
    "oms_order_block": {
        "uri_path": "/ims/service/oms/business/add/block",
        "method": "post",
        "data": {
            "functionType": "4",
            "goodsSkuList": [
                {
                    "goodsSkuCode": "P68687174",
                    "qty": 4,
                }
            ],
            "operateType": "2",
            "operatorId": 8,
            "sourceNo": "CG21090310010",
            "warehouseId": 19
        }
    },

    "purchase_create_order": {
        "uri_path": "/ims/service/scm/business/goods/sku",
        "method": "post",
        "data": [
            {
                "functionType": "26",
                "goodsSkuList": [
                    {
                        "goodsSkuCode": "P68687174",
                        "qty": 4,
                        "targetWarehouseId": "19"
                    }
                ],
                "operateType": "1",
                "operatorId": 8,
                "sourceNo": "CG21090310010",
                "warehouseId": 19
            }
        ]
    },
    "purchase_into_warehouse": {
        "uri_path": "/ims/service/wms/business/purchase/into/warehouse",
        "method": "post",
        "data": {
            "functionType": "1",
            "goodsSkuList": [
                {
                    "bomVersion": "2",
                    "goodsSkuCode": "P68687174",
                    "wareSkuList": [
                        {
                            "bomQty": 4,
                            "qty": 16,
                            "storageLocationId": 743,
                            "storageLocationType": 5,
                            "wareSkuCode": "W03278514"
                        },
                        {
                            "bomQty": 3,
                            "qty": 12,
                            "storageLocationId": 731,
                            "storageLocationType": 5,
                            "wareSkuCode": "W83173944"
                        }
                    ]
                }
            ],
            "operateType": "1",
            "operatorId": 8,
            "sourceNo": "CG21090310010",
            "targetWarehouseId": "19",
            "warehouseId": 19
        }
    },
    "other_into_warehouse": {
        "uri_path": "/ims/service/wms/business/other/into/warehouse",
        "method": "post",
        "data": [
            {
                "functionType": "2",
                "operateType": "1",
                "operatorId": 8,
                "sourceNo": "RK210906001",
                "targetWarehouseId": "19",
                "wareSkuList": [
                    {
                        "qty": 8,
                        "storageLocationId": 731,
                        "storageLocationType": 5,
                        "wareSkuCode": "W03278514"
                    }
                ],
                "warehouseId": 19
            }
        ]
    },
    "delivery_order_block": {
        "uri_path": "/ims/service/wms/business/add/sale/block",
        "method": "post",
        "data": {
            "functionType": "4",
            "goodsSkuList": [
                {
                    "goodsSkuCode": "P68687174",
                    "qty": 1
                }
            ],
            "operateType": "2",
            "operatorId": 8,
            "sourceNo": "CK2109031022",
            "targetWarehouseId": 19,
            "warehouseId": 19
        }
    },
    "assign_location_stock": {
        "uri_path": "/ims/service/wms/business/distribute/ware/block",
        "method": "post",
        "data": [
            {
                "functionType": "4",
                "operateType": "2",
                "operatorId": 8,
                "sourceNo": "CK2109040073",
                "wareSkuList": [
                    {
                        "qty": 3,
                        "wareSkuCode": "W83173944"
                    },
                    {
                        "qty": 4,
                        "wareSkuCode": "W03278514"
                    }
                ],
                "warehouseId": 19
            }
        ]
    },
    "confirm_pick": {
        "uri_path": "/ims/service/wms/business/pick/ware/sku",
        "method": "post",
        "data": {
            "functionType": "15",
            "operateType": "4",
            "operatorId": 8,
            "sourceNo": "CK2109040073",
            "wareSkuList": [
                {
                    "wareSkuCode": "W83173944",
                    "qty": 3,
                    "storageLocationId": "743"
                },
                {
                    "wareSkuCode": "W03278514",
                    "qty": 4,
                    "storageLocationId": "731"
                }
            ],
            "warehouseId": "19"
        }
    },
    "delivery_out": {
        "uri_path": "/ims/service/wms/business/out/of/stock",
        "method": "post",
        "data": [
            {
                "functionType": "17",
                "operateType": "5",
                "operatorId": 8,
                "sourceNo": "CK2109040073",
                "targetWarehouseId": 19,
                "wareSkuList": [
                    {
                        "qty": 3,
                        "storageLocationId": -19,
                        "wareSkuCode": "W83173944"
                    },
                    {
                        "qty": 4,
                        "storageLocationId": -19,
                        "wareSkuCode": "W03278514"
                    }
                ],
                "warehouseId": 19
            }
        ]
    },
    "cancel_oms_order_block": {
        "uri_path": "/ims/service/oms/business/rollback/block",
        "method": "post",
        "data": {
            "blockBookId": "",
            "functionType": "8",
            "operateType": "2",
            "operatorId": 8,
            "sourceNo": "CK2109040006"
        }
    },
    "cancel_block_before_pick": {
        "uri_path": "/ims/service/wms/business/rollback/ware/block",
        "method": "post",
        "data": {
            "functionType": "8",
            "operateType": "2",
            "operatorId": 8,
            "sourceNo": "CK2109040006"
        }
    },
    "cancel_block_after_pick": {
        "uri_path": "/ims/service/wms/business/rollback/pick/ware",
        "method": "post",
        "data": {
            "functionType": "8",
            "operateType": "2",
            "operatorId": 8,
            "sourceNo": "CK2109040068",
            "wareSkuList": [
                {
                    "fromStorageLocationId": -19,
                    "qty": 3,
                    "toStorageLocationId": 1194,
                    "toStorageLocationType": "4",
                    "toTargetWarehouseId": 19,
                    "wareSkuCode": "W83173944"
                },
                {
                    "fromStorageLocationId": -19,
                    "qty": 4,
                    "toStorageLocationId": 1197,
                    "toStorageLocationType": "4",
                    "toTargetWarehouseId": 19,
                    "wareSkuCode": "W03278514"
                }
            ]
        }
    },
    "qualified_goods_other_out_block": {
        "uri_path": "/ims/service/wms/business/distribute/transfer/block",
        "method": "post",
        "data": [
            {
                "functionType": "5",
                "operateType": "2",
                "operatorId": 8,
                "processType": 1,
                "sourceNo": "source210906002",
                "targetWarehouseId": 19,
                "wareSkuList": [

                    {
                        "qty": 3,
                        "storageLocationId": 731,
                        "wareSkuCode": "W03278514"
                    }
                ],
                "warehouseId": 19
            }
        ],
    },
    "unqualified_goods_other_out_block": {
        "uri_path": "/ims/service/wms/business/distribute/bad/block",
        "method": "post",
        "data": [
            {
                "functionType": "5",
                "operateType": "2",
                "operatorId": 8,
                "processType": 1,
                "sourceNo": "source210906002",
                "wareSkuList": [

                    {
                        "qty": 3,
                        "storageLocationId": 731,
                        "wareSkuCode": "W03278514"
                    }
                ],
                "warehouseId": 19
            }
        ]
    },
    "qualified_goods_other_out_delivery_goods": {
        "uri_path": "/ims/service/wms/business/out/of/other/stock",
        "method": "post",
        "data": [
            {
                "functionType": "39",
                "operateType": "5",
                "operatorId": 8,
                "processType": 1,
                "sourceNo": "sourceNo2109022001",
                "targetWarehouseId": 19,
                "wareSkuList": [
                    {
                        "qty": 2,
                        "storageLocationId": 743,
                        "wareSkuCode": "W83173944"
                    }
                ],
                "warehouseId": 19
            }
        ]
    },
    "unqualified_goods_other_out_delivery_goods": {
        "uri_path": "/ims/service/wms/business/out/of/bad",
        "method": "post",
        "data": [
            {
                "functionType": "39",
                "operateType": "5",
                "operatorId": 8,
                "processType": 1,
                "sourceNo": "sourceNo2109022001",
                "wareSkuList": [
                    {
                        "qty": 2,
                        "storageLocationId": 743,
                        "wareSkuCode": "W83173944"
                    }
                ],
                "warehouseId": 19
            }
        ]
    },
    "cancel_unqualified_goods_other_out_block": {
        "uri_path": "/ims/service/wms/business/rollback/bad/block",
        "method": "post",
        "data": {
            "blockBookId": "",
            "functionType": 40,
            "operateType": 3,
            "operatorId": 8,
            "sourceNo": ""
        }
    },
    "cancel_qualified_goods_other_out_block": {
        "uri_path": "/ims/service/wms/business/rollback/other/block",
        "method": "post",
        "data": {
            "blockBookId": "",
            "functionType": 40,
            "operateType": 3,
            "operatorId": 8,
            "sourceNo": ""
        }
    },
    "turn_to_unqualified_goods": {
        "uri_path": "/ims/service/stock/manage/bad",
        "method": "post",
        "data":
            {
                "fromStorageLocationId": 153,
                "functionType": "20",
                "operateType": "6",
                "operatorId": 8,
                "qty": 1,
                "sourceNo": "YK1442748295833251842",
                "targetWarehouseId": 31,
                "toStorageLocationId": 631,
                "toStorageLocationType": 6,
                "wareSkuCode": "11471839197A01",
                "warehouseId": 31
            }
    }
}
