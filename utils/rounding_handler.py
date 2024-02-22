import decimal


class Rounding:
    """数值取整"""

    @staticmethod
    def round_up(num, precision):
        """向上取整"""
        num_decimal = decimal.Decimal(str(num))
        precision_decimal = decimal.Decimal(str(precision))
        factor = decimal.Decimal(1) / precision_decimal
        rounded_decimal = (num_decimal * factor).to_integral_value(rounding=decimal.ROUND_CEILING)
        rounded_decimal /= factor
        rounded_decimal = rounded_decimal.quantize(precision_decimal, rounding=decimal.ROUND_CEILING)
        return float(rounded_decimal)

    @staticmethod
    def round_down(num, precision):
        """向下取整"""
        num_decimal = decimal.Decimal(str(num))
        precision_decimal = decimal.Decimal(str(precision))
        factor = decimal.Decimal(1) / precision_decimal
        rounded_decimal = (num_decimal * factor).to_integral_value(rounding=decimal.ROUND_FLOOR)
        rounded_decimal /= factor
        rounded_decimal = rounded_decimal.quantize(precision_decimal, rounding=decimal.ROUND_FLOOR)
        return float(rounded_decimal)

    @staticmethod
    def round_half_up(num, precision):
        """四舍五入"""
        num_decimal = decimal.Decimal(str(num))
        precision_decimal = decimal.Decimal(str(precision))
        factor = decimal.Decimal(1) / precision_decimal
        rounded_decimal = (num_decimal * factor).to_integral_value(rounding=decimal.ROUND_HALF_EVEN)
        rounded_decimal /= factor
        rounded_decimal = rounded_decimal.quantize(precision_decimal, rounding=decimal.ROUND_HALF_EVEN)
        return float(rounded_decimal)

    @classmethod
    def do_round(cls, round_mode, num, precision):
        if round_mode == "ROUND_UP":
            return cls.round_up(num, precision)
        elif round_mode == "ROUND_DOWN":
            return cls.round_down(num, precision)
        elif round_mode == "ROUND_OFF":
            return cls.round_half_up(num, precision)
        else:
            raise ValueError("取整方式枚举错误！")
