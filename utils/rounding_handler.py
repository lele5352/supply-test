import decimal


class Rounding:
    """数值取整"""

    @classmethod
    def round_up(cls, num, precision):
        """向上取整"""
        num_decimal = decimal.Decimal(str(num))
        precision_decimal = decimal.Decimal(str(precision))
        factor = decimal.Decimal(1) / precision_decimal
        rounded_decimal = (num_decimal * factor).to_integral_value(rounding=decimal.ROUND_CEILING)
        rounded_decimal /= factor
        rounded_decimal = rounded_decimal.quantize(precision_decimal, rounding=decimal.ROUND_CEILING)
        return rounded_decimal

    @classmethod
    def round_down(cls, num, precision):
        """向下取整"""
        num_decimal = decimal.Decimal(str(num))
        precision_decimal = decimal.Decimal(str(precision))
        factor = decimal.Decimal(1) / precision_decimal
        rounded_decimal = (num_decimal * factor).to_integral_value(rounding=decimal.ROUND_FLOOR)
        rounded_decimal /= factor
        rounded_decimal = rounded_decimal.quantize(precision_decimal, rounding=decimal.ROUND_FLOOR)
        return rounded_decimal

    @classmethod
    def round_half_up(cls, num, precision):
        """四舍五入"""
        num_decimal = decimal.Decimal(str(num))
        precision_decimal = decimal.Decimal(str(precision))
        factor = decimal.Decimal(1) / precision_decimal
        rounded_decimal = (num_decimal * factor).to_integral_value(rounding=decimal.ROUND_HALF_EVEN)
        rounded_decimal /= factor
        rounded_decimal = rounded_decimal.quantize(precision_decimal, rounding=decimal.ROUND_HALF_EVEN)
        return rounded_decimal
