from enum import Enum


class Unit(Enum):
    INTERNATIONAL = 10
    IMPERIAL = 20


class ItemType(Enum):
    SIZE = "SIZE"
    WEIGHT = "WEIGHT"
    VOLUME = "VOLUME"


class UnitChange:
    """单位换算"""

    @staticmethod
    def cm_to_in(number):
        return number * 0.393700787402

    @staticmethod
    def cm3_to_in3(number):
        return number * 0.0610238

    @staticmethod
    def kg_to_lb(number):
        return number * 2.204622

    @staticmethod
    def in_to_cm(number):
        return number * 2.539950

    @staticmethod
    def in3_to_cm3(number):
        return number * 16.387037

    @staticmethod
    def lb_to_kg(number):
        return number * 0.45359237

    @classmethod
    def change(cls, num, num_type, source_unit, target_unit) -> float:
        """执行转换
        :param float num: 数值
        :param string num_type:数值类型
        :param int source_unit:原单位
        :param int target_unit:目标单位
        """
        # 处理大小写差异，统一转大写去匹配数值类型枚举
        num_type = num_type.upper()
        change_map = {
            (Unit.INTERNATIONAL.value, ItemType.SIZE.value): UnitChange.in_to_cm,
            (Unit.INTERNATIONAL.value, ItemType.WEIGHT.value): UnitChange.lb_to_kg,
            (Unit.INTERNATIONAL.value, ItemType.VOLUME.value): UnitChange.in3_to_cm3,
            (Unit.IMPERIAL.value, ItemType.SIZE.value): UnitChange.cm_to_in,
            (Unit.IMPERIAL.value, ItemType.WEIGHT.value): UnitChange.kg_to_lb,
            (Unit.IMPERIAL.value, ItemType.VOLUME.value): UnitChange.cm3_to_in3,
        }
        if source_unit == target_unit:
            return num
        change_function = change_map.get((target_unit, num_type))
        if change_function:
            return change_function(num)
        else:
            raise KeyError("转换失败：单位或数值类型不正确！")


if __name__ == '__main__':
    uc = UnitChange()
    result = uc.change(115.666, "weight", 10, 20)
    print(result)
