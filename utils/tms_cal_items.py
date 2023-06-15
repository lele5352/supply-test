from utils.unit_change_handler import *
from utils.rounding_handler import *


class TMSCalcItems:
    """TMS货物计量项"""

    def __init__(self, weight, length, width, height):
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height

    def longest_side(self):
        """最长边"""
        sides = [self.length, self.width, self.height]
        sides.sort(reverse=True)
        return sides[0]

    def mid_side(self):
        """第二长边"""
        sides = [self.length, self.width, self.height]
        sides.sort(reverse=True)
        return sides[1]

    def shortest_side(self):
        """最短边"""
        sides = [self.length, self.width, self.height]
        sides.sort(reverse=True)
        return sides[2]

    def girth(self):
        """围长"""
        return self.longest_side() + (self.mid_side() + self.shortest_side()) * 2

    def perimeter(self):
        """周长"""
        return self.longest_side() + self.mid_side() + self.shortest_side()

    def two_sides_length(self):
        """两边长=最长边+次长边=长+宽"""
        return self.longest_side() + self.mid_side()

    def volume(self):
        """体积=长*宽*高"""
        return self.longest_side() * self.mid_side() * self.shortest_side()

    def volume_weight(self, precision):
        """体积重=(长*宽*高)/体积重系数"""
        return round(self.volume() / precision, 2)

    def density(self, unit_change=False):
        """美卡托盘密度"""
        if unit_change:
            # 判断是否需要换算单位，若货物信息的单位为国际单位，则需要换算，传True
            weight = UnitChange.change(self.weight, "weight", "gj", "yz")
            volume = UnitChange.change(self.volume(), "volume", "gj", "yz") / 1728
            density = weight / volume
            return density
        return self.weight / self.volume() * 1728


class GoodsMeasurementItems:
    """货物计量项信息"""

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

    def origin_items(self):
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

    def unit_changed_items(self):
        return {
            x: UnitChange.change(
                self.origin_items().get(x).get("num"),
                self.origin_items().get(x).get("num_type"),
                self.source_unit, self.target_unit)
            for x in self.origin_items()
        }

    def rounded_result(self):
        temp_dict = dict()

        for item in self.unit_changed_items():
            if item == "重量":
                if self.weight_rounding == "向上取整":
                    temp_dict[item] = Rounding.round_up(self.unit_changed_items().get(item), self.weight_precision)
                elif self.weight_rounding == "向下取整":
                    temp_dict[item] = Rounding.round_down(self.unit_changed_items().get(item), self.weight_precision)
                else:
                    temp_dict[item] = Rounding.round_half_up(self.unit_changed_items().get(item),
                                                             self.weight_precision)
            else:
                if self.size_rounding == "向上取整":
                    temp_dict[item] = Rounding.round_up(self.unit_changed_items().get(item), self.size_precision)

                elif self.size_rounding == "向下取整":
                    temp_dict[item] = Rounding.round_down(self.unit_changed_items().get(item), self.size_precision)
                else:
                    temp_dict[item] = Rounding.round_half_up(self.unit_changed_items().get(item), self.size_precision)
        return temp_dict


def package_calc(goods_info_list, precision):
    temp_result = [0, 0, 0]
    temp_weight = 0
    for length, width, height, weight in goods_info_list:
        sides = [length, width, height]
        sides.sort(reverse=True)
        temp_result = [max(temp_result[0], sides[0]), max(temp_result[1], sides[1]), temp_result[2] + sides[2]]
        temp_result.sort(reverse=True)
        temp_weight += weight
    temp_result.append(round(temp_weight, 6))
    items = TMSCalcItems(temp_result[3], temp_result[0], temp_result[1], temp_result[2])
    grith = items.girth()
    volume_weight = items.volume_weight(precision)
    temp_result.extend([grith, volume_weight])

    return temp_result


if __name__ == '__main__':
    # no_pack_goods_list = [
    #     (22.2, 99.9, 33.3, 9.99),
    #     (22.2, 55.5, 33.3, 1.22),
    #     (22.2, 55.5, 33.3, 1.22),
    #     (11.1, 55.5, 44.4, 3.11),
    #     (11.1, 55.5, 44.4, 3.11)
    #
    # ]
    # pack_goods_list = [
    #     (11.1, 55.5, 44.4, 3.11),
    #     (22.2, 55.5, 33.3, 1.22),
    #     (22.2, 55.5, 33.3, 1.22)
    #
    # ]
    # print(package_calc(no_pack_goods_list, 2000))
    # print(package_calc(pack_goods_list, 2200))
    goods_info = {
            "weight": 99.00,
            "length": 9.0,
            "width": 31.0,
            "height": 89.0
    }
    # 货物单位
    goods_unit = "yz"
    # 渠道单位
    channel_unit = "gj"
    # 渠道重量取整方式
    channel_weight_rounding = "向上取整"
    # 渠道重量取整精度
    channel_weight_rounding_precision = 1
    # 渠道尺寸取整方式
    channel_size_rounding = "向上取整"
    # 渠道尺寸取整精度
    channel_size_rounding_precision = 1

    goods_items = GoodsMeasurementItems(goods_info, goods_unit, channel_unit, channel_weight_rounding,
                                        channel_weight_rounding_precision, channel_size_rounding,
                                        channel_size_rounding_precision)

    # print("{}转{}单位换算结果：".format(goods_unit, channel_unit))
    # for i in item.origin_result():
    #     print("{}：{}，{}".format(i, item.origin_result().get(i).get("num"), item.unit_changed_result().get(i)))
    print(
        "重量{}取整精度{},尺寸{}取整精度{}取整结果：".format(channel_weight_rounding, channel_weight_rounding_precision,
                                                            channel_size_rounding, channel_size_rounding_precision))
    for i in goods_items.origin_items():
        print("{}：{}".format(i, goods_items.rounded_result().get(i)))
