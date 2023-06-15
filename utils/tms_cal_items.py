from utils.rounding_handler import *
from utils.unit_change_handler import *


class TMSCalcItems:
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
        """两边长，最长边+次长边"""
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
    items = TMSCalcItems(24.31, 66.6, 44.4, 199.9)
    no_pack_goods_list = [
        (22.2, 99.9, 33.3, 9.99),
        (22.2, 55.5, 33.3, 1.22),
        (22.2, 55.5, 33.3, 1.22),
        (11.1, 55.5, 44.4, 3.11),
        (11.1, 55.5, 44.4, 3.11)

    ]
    pack_goods_list = [
        (11.1, 55.5, 44.4, 3.11),
        (22.2, 55.5, 33.3, 1.22),
        (22.2, 55.5, 33.3, 1.22)

    ]
    print(package_calc(no_pack_goods_list, 2000))
    print(package_calc(pack_goods_list, 2200))
