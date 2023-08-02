import decimal
from json import JSONEncoder

"""
json 自定义转换类型
"""


class DecimalEncoder(JSONEncoder):
    """
    用于 json 序列化 时处理 decimal 类型
    """
    def __init__(self, decimal_places=2, decimal_round=None, *args, **kwargs):
        """
        :param decimal_places: int ，用于指定保留的小数位数
        :param decimal_round: str ，用于指定decimal 取值方式，为空时默认为 ROUND_HALF_UP
        """
        self.decimal_places = decimal_places
        self.decimal_round = decimal_round or decimal.ROUND_HALF_UP

        super().__init__(*args, **kwargs)

    def default(self, o):
        if isinstance(o, decimal.Decimal):
            # 将 Decimal 类型转换为指定小数位数的字符串，再转换为 float 类型
            return float(
                o.quantize(decimal.Decimal("0.{}".format("0" * self.decimal_places)),
                           rounding=self.decimal_round)
            )
        return super().default(o)