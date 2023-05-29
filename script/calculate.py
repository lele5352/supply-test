import math


def round_up(num, precision):
    factor = 1 / precision
    return math.ceil(num * factor) / factor


def round_down(num, precision):
    factor = 1 / precision
    return math.floor(num * factor) / factor


def round_num(num, precision):
    factor = 1 / precision
    return round(num * factor) / factor


def calculate(method, num, precision):
    if method == "向上取整":
        return round_up(num, precision)
    elif method == "向下取整":
        return round_down(num, precision)
    elif method == "四舍五入":
        return round_num(num, precision)
    else:
        pass


def unit_change(number, source_unit, target_unit):
    if source_unit == target_unit:
        return number
    if source_unit == "cm" and target_unit == "in":
        return number * 0.393707
    elif source_unit == "in" and target_unit == "cm":
        return number * 2.539950
    elif source_unit == "cm3" and target_unit == "in3":
        return number * 0.0610238
    elif source_unit == "in3" and target_unit == "cm3":
        return number * 16.387037
    elif source_unit == "kg" and target_unit == "lb":
        return number * 2.204622
    elif source_unit == "lb" and target_unit == "kg":
        return number * 0.453592


def wei_chang(length, width, height):
    result = length + (width + height) * 2
    return result


def zhou_chang(length, width, height):
    result = length + width + height
    return result


def liang_bian_chang(length, width):
    result = length + width
    return result


def volume(length, width, height):
    result = length * width * height
    return result


precisions = [1, 0.1, 0.5, 0.01, 0.05]
sizes = [
    (9.0, 31.0, 89.0),
    (9.1, 31.1, 89.1),
    (9.4, 31.4, 89.4),
    (9.5, 31.5, 89.5),
    (9.9, 31.9, 89.9)]
weights = [99.00, 99.01, 99.49, 99.50, 99.99]
methods = ["四舍五入"]  # "向下取整", "四舍五入

len_source_unit = "in"
len_target_unit = "cm"

volume_source_unit = "in3"
volume_target_unit = "cm3"

weight_source_unit = "lb"
weight_target_unit = "kg"

for method in methods:
    for precision in precisions:
        print("取整方式：{}，取整精度:{}".format(method, precision))
        for weight, size in zip(weights, sizes):
            unit_changed_weight = unit_change(weight, weight_source_unit, weight_target_unit)
            rounded_weight = calculate(method, unit_changed_weight, precision)
            print("原始重量为：{}，单位换算后为：{}，取整后为：{}".format(weight, unit_changed_weight, rounded_weight))

            unit_changed_length = unit_change(size[2], len_source_unit, len_target_unit)
            rounded_length = calculate(method, unit_changed_length, precision)
            print("原始长为：{}，单位换算后为：{}，取整后为：{}".format(size[2], unit_changed_length, rounded_length))

            unit_changed_width = unit_change(size[1], len_source_unit, len_target_unit)
            rounded_width = calculate(method, unit_changed_width, precision)
            print("原始宽为：{}，单位换算后为：{}，取整后为：{}".format(size[1], unit_changed_width, rounded_width))

            unit_changed_height = unit_change(size[0], len_source_unit, len_target_unit)
            rounded_height = calculate(method, unit_changed_height, precision)
            print("原始高为：{}，单位换算后为：{}，取整后为：{}".format(size[0], unit_changed_height, rounded_height))

            origin_wei_chang = wei_chang(size[2], size[1], size[0])
            unit_changed_wei_chang = unit_change(origin_wei_chang, len_source_unit, len_target_unit)
            rounded_wei_chang = calculate(method, unit_changed_wei_chang, precision)
            print("原始围长为：{}，单位换算后为：{}，取整后为：{}".format(origin_wei_chang, unit_changed_wei_chang,
                                                                     rounded_wei_chang))

            origin_zhou_chang = zhou_chang(size[2], size[1], size[0])
            unit_changed_zhou_chang = unit_change(origin_zhou_chang, len_source_unit, len_target_unit)
            rounded_zhou_chang = calculate(method, unit_changed_zhou_chang, precision)
            print("原始周长为：{}，单位换算后为：{}，取整后为：{}".format(origin_zhou_chang, unit_changed_zhou_chang,
                                                                     rounded_zhou_chang))

            origin_liang_bian_chang = liang_bian_chang(size[2], size[1])
            unit_changed_liang_bian_chang = unit_change(origin_liang_bian_chang, len_source_unit, len_target_unit)
            rounded_liang_bian_chang = calculate(method, unit_changed_liang_bian_chang, precision)
            print("原始两边为：{}，单位换算后为：{}，取整后为：{}".format(origin_liang_bian_chang,
                                                                     unit_changed_liang_bian_chang,
                                                                     rounded_liang_bian_chang))

            origin_volume = volume(size[2], size[1], size[0])
            unit_changed_volume = unit_change(origin_volume, volume_source_unit, volume_target_unit)
            rounded_volume = calculate(method, unit_changed_volume, precision)
            print(
                "原始体积为：{}，单位换算后为：{}，取整后为：{}".format(origin_volume, unit_changed_volume, rounded_volume))
            print("----------------------------------------------------------------------")
