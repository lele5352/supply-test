from utils.calculate import *
from utils.tms_cal_items import *

if __name__ == '__main__':
    length = 11
    width = 11
    height = 11
    weight = 11

    origin_len_unit = "cm"
    origin_weight_unit = "kg"
    origin_volume_unit = "cm3"

    target_len_unit = "in"
    target_weight_unit = "lb"
    target_volume_unit = "in3"

    origin_volume = volume(length, width, height)
    unit_changed_volume = unit_change(origin_volume, origin_volume_unit, "in3")

    unit_changed_weight = unit_change(weight, "kg", "lb")

    density = density(unit_changed_weight,unit_changed_volume)

    print(density)