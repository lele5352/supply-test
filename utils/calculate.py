import decimal


def round_up(num, precision):
    num_decimal = decimal.Decimal(str(num))
    precision_decimal = decimal.Decimal(str(precision))
    rounded_decimal = num_decimal.quantize(precision_decimal, rounding=decimal.ROUND_CEILING)
    return rounded_decimal


def round_down(num, precision):
    num_decimal = decimal.Decimal(str(num))
    precision_decimal = decimal.Decimal(str(precision))
    rounded_decimal = num_decimal.quantize(precision_decimal, rounding=decimal.ROUND_FLOOR)
    return rounded_decimal


def round_half_up(num, precision):
    num_decimal = decimal.Decimal(str(num))
    precision_decimal = decimal.Decimal(str(precision))
    rounded_decimal = num_decimal.quantize(precision_decimal, rounding=decimal.ROUND_HALF_EVEN)
    return rounded_decimal


def calculate(method, num, precision):
    if method == "向上取整":
        return round_up(num, precision)
    elif method == "向下取整":
        return round_down(num, precision)
    elif method == "四舍五入":
        return round_half_up(num, precision)
    else:
        pass


def unit_change(number, source_unit, target_unit):
    """

    @param number: 参数值
    @param source_unit: 被转换单位
    @param target_unit: 目标单位
    @return:
    """
    # 浮点数计算会有精度丢失问题，取整6位小数处理
    if source_unit == target_unit:
        return round(number, 6)
    if source_unit == "cm" and target_unit == "in":
        return round(number * 0.393700787402, 6)
    elif source_unit == "in" and target_unit == "cm":
        return round(number * 2.539950, 6)
    elif source_unit == "cm3" and target_unit == "in3":
        return round(number * 0.0610238, 6)
    elif source_unit == "in3" and target_unit == "cm3":
        return round(number * 16.387037, 6)
    elif source_unit == "kg" and target_unit == "lb":
        return round(number * 2.204622, 6)
    elif source_unit == "lb" and target_unit == "kg":
        return round(number * 0.453592, 6)


class UnitChange:
    class InternationalToImperial:
        @classmethod
        def length(cls, number):
            return number * 0.393700787402

        @classmethod
        def volume(cls, number):
            return number * 0.0610238

        @classmethod
        def weight(cls, number):
            return number * 2.204622

    class ImperialToInternational:
        @classmethod
        def length(cls, number):
            return number * 2.539950

        @classmethod
        def volume(cls, number):
            return number * 16.387037

        @classmethod
        def weight(cls, number):
            return number * 0.453592
