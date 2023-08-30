from data_generator.transfer_data_generator import WmsTransferDataGenerator
from data_generator.scm_data_generator import ScmDataGenerator
from data_generator.pms_data_generator import create_spu
from robot_run.run_transfer import run_transfer
from robot_run.run_receive import run_receive

sale_sku = create_spu(productName="测试单品单件", package_num=1, single_package_num=1)
transfer_stock = [
    {

        "trans_out_id": 512,
        "trans_out_to_id": 0,
        "trans_in_id": 565,
        "trans_in_to_id": 0,
        "sale_sku": sale_sku,
        "bom": "A",
        "qty": 1,
        "inventory_type": 10,  # 现货10，在途20
        "up_shelf_mode": "box",
        "flow_flag": None
    },
    {
        "trans_out_id": 640,
        "trans_out_to_id": 0,
        "trans_in_id": 565,
        "trans_in_to_id": 0,
        "sale_sku": sale_sku,
        "bom": "A",
        "qty": 2,
        "inventory_type": 10,  # 现货10，在途20
        "up_shelf_mode": "sku",
        "flow_flag": None
    },
    {
        "trans_out_id": 512,
        "trans_out_to_id": 0,
        "trans_in_id": 565,
        "trans_in_to_id": 0,
        "sale_sku": sale_sku,
        "bom": "A",
        "qty": 3,
        "inventory_type": 20,  # 现货10，在途20
        "up_shelf_mode": "",
        "flow_flag": "handover"
    },
    {
        "trans_out_id": 640,
        "trans_out_to_id": 0,
        "trans_in_id": 565,
        "trans_in_to_id": 0,
        "sale_sku": sale_sku,
        "bom": "A",
        "qty": 4,
        "inventory_type": 20,  # 现货10，在途20
        "up_shelf_mode": "",
        "flow_flag": "received"
    },
{

        "trans_out_id": 512,
        "trans_out_to_id": 0,
        "trans_in_id": 639,
        "trans_in_to_id": 639,
        "sale_sku": sale_sku,
        "bom": "A",
        "qty": 1,
        "inventory_type": 10,  # 现货10，在途20
        "up_shelf_mode": "box",
        "flow_flag": None
    },
    {
        "trans_out_id": 640,
        "trans_out_to_id": 0,
        "trans_in_id": 639,
        "trans_in_to_id": 639,
        "sale_sku": sale_sku,
        "bom": "A",
        "qty": 2,
        "inventory_type": 10,  # 现货10，在途20
        "up_shelf_mode": "sku",
        "flow_flag": None
    },
    {
        "trans_out_id": 512,
        "trans_out_to_id": 0,
        "trans_in_id": 639,
        "trans_in_to_id": 639,
        "sale_sku": sale_sku,
        "bom": "A",
        "qty": 3,
        "inventory_type": 20,  # 现货10，在途20
        "up_shelf_mode": "",
        "flow_flag": "handover"
    },
    {
        "trans_out_id": 640,
        "trans_out_to_id": 0,
        "trans_in_id": 639,
        "trans_in_to_id": 639,
        "sale_sku": sale_sku,
        "bom": "A",
        "qty": 4,
        "inventory_type": 20,  # 现货10，在途20
        "up_shelf_mode": "",
        "flow_flag": "received"
    }
]
purchase_stock = [
    {
        "qty": 5,
        "delivery_warehouse_code": "ESBH2",
        "target_warehouse_code": "",
        "sale_sku": [sale_sku]
    },
    {
        "qty": 6,
        "delivery_warehouse_code": "ESBH2",
        "target_warehouse_code": "",
        "sale_sku": [sale_sku]
    },
{
        "qty": 5,
        "delivery_warehouse_code": "HWZF",
        "target_warehouse_code": "HWZF",
        "sale_sku": [sale_sku]
    },
    {
        "qty": 6,
        "delivery_warehouse_code": "HWZF",
        "target_warehouse_code": "HWZF",
        "sale_sku": [sale_sku]
    }
]


def main():
    trans_data = WmsTransferDataGenerator()
    scm_data = ScmDataGenerator()
    for item in transfer_stock:
        demand_no = trans_data.create_transfer_demand(
            item["trans_out_id"], item["trans_out_to_id"], item["trans_in_id"],
            item["trans_in_to_id"], item["sale_sku"], item["bom"], item["qty"]
        )
        if item["inventory_type"] == 10:
            result, info = run_transfer(demand_no, up_shelf_mode=item["up_shelf_mode"])
            print(result, info)
        else:
            result, info = run_transfer(demand_no, item["flow_flag"])
            print(result, info)
    for item in purchase_stock:
        result_list = scm_data.create_distribute_order(
            item["sale_sku"], item["qty"], item["delivery_warehouse_code"], item["target_warehouse_code"])
        source_order_list = [_[0] for _ in result_list]
        for order in source_order_list:
            result, info = run_receive(order)
            print(result, info)


if __name__ == '__main__':
    main()
