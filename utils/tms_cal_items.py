import decimal


class Rounding:
    """数值取整"""

    @classmethod
    def round_up(cls, num, precision):
        num_decimal = decimal.Decimal(str(num))
        precision_decimal = decimal.Decimal(str(precision))
        factor = decimal.Decimal(1) / precision_decimal
        rounded_decimal = (num_decimal * factor).to_integral_value(rounding=decimal.ROUND_CEILING)
        rounded_decimal /= factor
        rounded_decimal = rounded_decimal.quantize(precision_decimal, rounding=decimal.ROUND_CEILING)
        return rounded_decimal

    @classmethod
    def round_down(cls, num, precision):
        num_decimal = decimal.Decimal(str(num))
        precision_decimal = decimal.Decimal(str(precision))
        factor = decimal.Decimal(1) / precision_decimal
        rounded_decimal = (num_decimal * factor).to_integral_value(rounding=decimal.ROUND_FLOOR)
        rounded_decimal /= factor
        rounded_decimal = rounded_decimal.quantize(precision_decimal, rounding=decimal.ROUND_FLOOR)
        return rounded_decimal

    @classmethod
    def round_half_up(cls, num, precision):
        num_decimal = decimal.Decimal(str(num))
        precision_decimal = decimal.Decimal(str(precision))
        factor = decimal.Decimal(1) / precision_decimal
        rounded_decimal = (num_decimal * factor).to_integral_value(rounding=decimal.ROUND_HALF_EVEN)
        rounded_decimal /= factor
        rounded_decimal = rounded_decimal.quantize(precision_decimal, rounding=decimal.ROUND_HALF_EVEN)
        return rounded_decimal


class UnitChange:
    @classmethod
    def cm_to_in(cls, number):
        return number * 0.393700787402

    @classmethod
    def cm3_to_in3(cls, number):
        return number * 0.0610238

    @classmethod
    def kg_to_lb(cls, number):
        return number * 2.204622

    @classmethod
    def in_to_cm(cls, number):
        return number * 2.539950

    @classmethod
    def in3_to_cm3(cls, number):
        return number * 16.387037

    @classmethod
    def lb_to_kg(cls, number):
        return number * 0.453592

    @classmethod
    def change(cls, num, num_type, source_unit, target_unit):
        """执行转换"""
        if source_unit == target_unit:
            return num
        elif target_unit == "gj":
            if num_type == "size":
                return cls.in_to_cm(num)
            elif num_type == "weight":
                return cls.lb_to_kg(num)
            elif num_type == "volume":
                return cls.in3_to_cm3(num)
            else:
                return "error"
        elif target_unit == "yz":
            if num_type == "size":
                return cls.cm_to_in(num)
            elif num_type == "weight":
                return cls.kg_to_lb(num)
            elif num_type == "volume":
                return cls.cm3_to_in3(num)
            else:
                return "error"
        else:
            return "error"


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

    def volume_weight(self,precision ):
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


def package_calc(goods_info_list,precision):
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
    # print("grith:{}".format(Rounding.round_up(items.girth(), 1)))
    # print("longestEdge:{}".format(Rounding.round_up(items.longest_side(), 1)))
    # print("perimeter:{}".format(Rounding.round_up(items.perimeter(), 1)))
    # print("secondSide:{}".format(Rounding.round_up(items.mid_side(), 1)))
    # print("shortestSide:{}".format(Rounding.round_up(items.shortest_side(), 1)))
    # print("sideLength:{}".format(Rounding.round_up(items.two_sides_length(), 1)))
    # print("volume:{}".format(Rounding.round_up(items.volume(), 1)))
    # print("weight:{}".format(Rounding.round_up(items.weight, 1)))
    # print("volume_weight:{}".format(round(items.volume_weight(), 2)))
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
    print(package_calc(no_pack_goods_list,2000))
    print(package_calc(pack_goods_list,2200))
