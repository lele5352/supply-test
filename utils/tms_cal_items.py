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
        sides = [self.length, self.width, self.height]
        sides.sort(reverse=True)
        return sides[0]

    def mid_side(self):
        sides = [self.length, self.width, self.height]
        sides.sort(reverse=True)
        return sides[1]

    def shortest_side(self):
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

    def density(self, unit_change=False):
        """美卡托盘密度"""
        if unit_change:
            weight = UnitChange.change(self.weight, "weight", "gj", "yz")
            volume = UnitChange.change(self.volume(), "volume", "gj", "yz")/1728
            density = weight / volume
            return density
        return self.weight / self.volume() * 1728


if __name__ == '__main__':
    items = TMSCalcItems(490, 99, 189, 31)
    print(items.density())
