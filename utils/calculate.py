from utils.tms_cal_items import *


class GoodsCalItem:
    def __init__(self, goods_info, goods_unit, channel_unit, weight_rounding, weight_precision, size_rounding,
                 size_precision):
        self.source_unit = goods_unit
        self.target_unit = channel_unit
        self.weight_rounding = weight_rounding
        self.weight_precision = weight_precision
        self.size_rounding = size_rounding
        self.size_precision = size_precision
        self.goods_info = goods_info
        self.tms_items = TMSCalcItems(**self.goods_info)

    def origin_result(self):
        return {
            "重量": {"num": self.goods_info.get("weight"), "num_type": "weight"},
            "最长边": {"num": self.tms_items.longest_side(), "num_type": "size"},
            "次长边": {"num": self.tms_items.mid_side(), "num_type": "size"},
            "最短边": {"num": self.tms_items.shortest_side(), "num_type": "size"},
            "围长": {"num": self.tms_items.girth(), "num_type": "size"},
            "周长": {"num": self.tms_items.perimeter(), "num_type": "size"},
            "两边长": {"num": self.tms_items.two_sides_length(), "num_type": "size"},
            "体积": {"num": self.tms_items.volume(), "num_type": "volume"}
        }

    def unit_changed_result(self):
        return {
            x: UnitChange.change(
                self.origin_result().get(x).get("num"),
                self.origin_result().get(x).get("num_type"),
                self.source_unit, self.target_unit)
            for x in self.origin_result()
        }

    def rounded_result(self):
        temp_dict = dict()

        for item in self.unit_changed_result():
            if item == "重量":
                if self.weight_rounding == "向上取整":
                    temp_dict[item] = Rounding.round_up(self.unit_changed_result().get(item), self.weight_precision)
                elif self.weight_rounding == "向下取整":
                    temp_dict[item] = Rounding.round_down(self.unit_changed_result().get(item), self.weight_precision)
                else:
                    temp_dict[item] = Rounding.round_half_up(self.unit_changed_result().get(item),
                                                             self.weight_precision)
            else:
                if self.size_rounding == "向上取整":
                    temp_dict[item] = Rounding.round_up(self.unit_changed_result().get(item), self.size_precision)

                elif self.size_rounding == "向下取整":
                    temp_dict[item] = Rounding.round_down(self.unit_changed_result().get(item), self.size_precision)
                else:
                    temp_dict[item] = Rounding.round_half_up(self.unit_changed_result().get(item), self.size_precision)
        return temp_dict


if __name__ == '__main__':
    goods_info = {
        "weight": 99.00,
        "length": 9.0,
        "width": 31.0,
        "height": 89.0
    }
    goods_unit = "yz"
    channel_unit = "gj"
    channel_weight_rounding = "向上取整"
    channel_weight_rounding_precision = 1
    channel_size_rounding = "向上取整"
    channel_size_rounding_precision = 1

    item = GoodsCalItem(goods_info, goods_unit, channel_unit, channel_weight_rounding,
                        channel_weight_rounding_precision, channel_size_rounding, channel_size_rounding_precision)

    print("{}转{}单位换算结果：".format(goods_unit, channel_unit))
    for i in item.origin_result():
        print("{}：{}，{}".format(i, item.origin_result().get(i).get("num"), item.unit_changed_result().get(i)))
    print(
        "重量{}取整精度{},尺寸{}取整精度{}取整结果：".format(channel_weight_rounding, channel_weight_rounding_precision,
                                                            channel_size_rounding, channel_size_rounding_precision))
    for i in item.origin_result():
        print("{}：{}".format(i, item.rounded_result().get(i)))
