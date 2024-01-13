class UnitChange:
    """单位换算"""

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
        return number * 0.45359237

    @classmethod
    def change(cls, num, num_type, source_unit, target_unit):

        """执行转换,10-国际单位,20英制单位
        """
        if source_unit == target_unit:
            return num
        elif target_unit == 10:
            if num_type == "size":
                return cls.in_to_cm(num)
            elif num_type == "weight":
                return cls.lb_to_kg(num)
            elif num_type == "volume":
                return cls.in3_to_cm3(num)
            else:
                return "error"
        elif target_unit == 20:
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