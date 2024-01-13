from utils.rounding_handler import *
from utils.unit_change_handler import UnitChange as UC


class PackageCalcItems:
    """获取包裹维度的各项维度数据，需要传入包裹维度的长、宽、高、实重；单件sku维度的最大实重、最小实重、最大长度、最小长度"""

    def __init__(self, length, width, height, weight, sku_list, volume_precision):
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.sku_list = sku_list
        self.volume_precision = volume_precision

    def longest_side(self):
        """最长边"""
        sides = [self.length, self.width, self.height]
        sides.sort(reverse=True)
        return round(sides[0], 6)

    def mid_side(self):
        """第二长边"""
        sides = [self.length, self.width, self.height]
        sides.sort(reverse=True)
        return round(sides[1], 6)

    def shortest_side(self):
        """最短边"""
        sides = [self.length, self.width, self.height]
        sides.sort(reverse=True)
        return round(sides[2], 6)

    def girth(self):
        """围长"""
        return round(self.length + (self.width + self.height) * 2, 6)

    def girth_origin(self):
        """围长,原始的 长+(宽+高)×2"""
        return self.length + (self.width + self.height) * 2

    def perimeter_origin(self):
        """三边长，原始长度  """
        return round(self.length + self.width + self.height, 6)

    def max_two_sides_length(self):
        """任意两边长"""
        sides_list = [self.length + self.width, self.length + self.height, self.width + self.height]
        sides_list.sort(reverse=True)
        return round(sides_list[0], 6)

    def mid_two_sides_length(self):
        """任意两边长"""
        sides_list = [self.length + self.width, self.length + self.height, self.width + self.height]
        sides_list.sort(reverse=True)
        return round(sides_list[1], 6)

    def min_two_sides_length(self):
        """任意两边长"""
        sides_list = [self.length + self.width, self.length + self.height, self.width + self.height]
        sides_list.sort(reverse=True)
        return round(sides_list[2], 6)

    def casual_two_sides_length(self):
        """任意两边长，长+宽；长+高；宽+高"""
        return {"长+宽": self.length + self.width, "长+高": self.length + self.height,
                "高+宽": self.width + self.height}

    def perimeter(self):
        """周长"""
        return round(self.longest_side() + self.mid_side() + self.shortest_side(), 6)

    def volume(self):
        """体积=长*宽*高"""
        return round(self.longest_side() * self.mid_side() * self.shortest_side(), 6)

    def volume_weight(self, precision):
        """体积重=(长*宽*高)/体积重系数"""
        return round(self.volume() / precision, 6)

    def bill_weight(self, precision):
        return max(self.weight, self.volume_weight(precision))

    def density(self, unit_change=False):
        """美卡托盘密度"""
        if unit_change:
            # 判断是否需要换算单位，若货物信息的单位为国际单位，则需要换算，传True
            weight = UC.change(self.weight, "weight", "10", "20")
            volume = UC.change(self.volume(), "volume", "10", "20") / 1728
            density = weight / volume
            return density
        return self.weight / self.volume() * 1728

    def package_items(self, source_unit, target_unit):
        package_items = {
            "weight": self.weight,
            "volumeWeight": self.volume_weight(self.volume_precision),
            "billWeight": max(self.volume_weight(self.volume_precision), self.weight),
            "longestEdge": self.longest_side(),
            "secondSide": self.mid_side(),
            "shortestEdge": self.shortest_side(),
            "girth": self.girth(),
            "perimeter": self.perimeter(),
            "maxSideLength": self.max_two_sides_length(),
            "midSideLength": self.mid_two_sides_length(),
            "minSideLength": self.min_two_sides_length(),
            "volume": self.volume(),
            "length": self.length,
            "width": self.width,
            "height": self.height,
            "skus": self.sku_list
        }
        if source_unit and target_unit and source_unit != target_unit:
            for item in package_items:
                if item in ["weight"]:
                    package_items[item] = round(UC.change(package_items[item], "weight", source_unit, target_unit), 6)
                elif item in ["volume", "volumeWeight"]:
                    package_items[item] = round(UC.change(package_items[item], "volume", source_unit, target_unit), 6)
                elif item in ["skus"]:
                    temp_list = list()
                    temp_list.extend(
                        [{
                            "skuMaxLength": round(UC.change(sku["skuMaxLength"], "size", source_unit, target_unit), 6),
                            "skuWeight": round(UC.change(sku["skuWeight"], "weight", source_unit, target_unit), 6)
                        } for sku in package_items[item]]
                    )
                    package_items[item] = temp_list
                elif item in ["billWeight"]:
                    # 计费重需要根据转换后的数值重置按大值赋值，不需要单位换算，上面已经换算过重量和体积重了
                    package_items[item] = max(package_items["weight"], package_items["volumeWeight"])
                else:
                    package_items[item] = round(UC.change(package_items[item], "size", source_unit, target_unit), 6)
        return package_items


class ChannelCalcItems:
    def __init__(self, goods_info, goods_unit, ch_unit, channel_calc_config, volume_precision):
        """
        渠道包裹信息换算
        :param list goods_info: 包裹维度的各项信息
        :param int goods_unit: 货物单位，10-国际，20-英制
        :param int ch_unit: 渠道单位，10-国际，20-英制
        :param dict channel_calc_config: 渠道配置的calc_info，从channel表读取
        :param float volume_precision: 体积重
        """
        self.source_unit = goods_unit
        self.ch_unit = ch_unit
        self.weight_rounding = channel_calc_config.get("weightRoundMode")
        self.weight_precision = channel_calc_config.get("weightRoundAccuracy")
        self.size_rounding = channel_calc_config.get("dimensionRoundMode")
        self.size_precision = channel_calc_config.get("dimensionRoundAccuracy")
        self.volume_precision = volume_precision
        self.tms_items = PackageCalcItems(*goods_info, volume_precision).package_items(self.source_unit, self.ch_unit)

    def rounded_result(self):
        temp_dict = dict()
        for item in self.tms_items:
            if item in ["weight", "volumeWeight", "billWeight"]:
                temp_dict[item] = Rounding.do_round(self.weight_rounding, self.tms_items.get(item), self.weight_precision)
            elif item in ["skus"]:
                temp_list = list()
                temp_list.extend([
                    {
                        "skuMaxLength": Rounding.do_round(self.size_rounding, i["skuMaxLength"], self.size_precision),
                        "skuWeight": Rounding.do_round(self.weight_rounding, i["skuWeight"], self.weight_precision)
                    } for i in self.tms_items[item]
                ])
                temp_dict[item] = temp_list
            else:
                temp_dict[item] = Rounding.do_round(self.size_rounding, self.tms_items.get(item), self.size_precision)
        return temp_dict


class CostPriceConversion:
    """成本价货物计量项信息"""
    """
            :param goods_info: dict {"weight": None, "length": None, "width":None, "height": None}
            :param goods_unit: string 国际单位 10 英制单位 20
            :param channel_unit: string 国际单位 10 英制单位 20
            :param weight_rounding: string 取整方式 "向上取整" "向下取整"
            :param weight_precision: string 取整精度 0.1 0.5 之类的
            :param size_rounding: string 取整方式 "向上取整" "向下取整"
            :param size_precision: string 取整精度 0.1 0.5 之类的
            """

    def __init__(self, goods_info, goods_unit, channel_unit, weight_rounding, weight_precision, size_rounding,
                 size_precision):
        self.source_unit = goods_unit
        self.target_unit = channel_unit
        self.weight_rounding = weight_rounding
        self.weight_precision = weight_precision
        self.size_rounding = size_rounding
        self.size_precision = size_precision
        self.goods_info = goods_info

    def unit_changed_items(self):
        """
        返回国际，英制单位的转化，{'weight': 27.0, 'length': 5.3, 'height': 5.3, 'width': 44.7}
        """
        temp_data = dict()
        for k, v in self.goods_info.items():
            num_type = "size" if k != "weight" else "weight"

            temp_data.update({k: UC.change(
                v, num_type,
                self.source_unit, self.target_unit)})
        print(temp_data)
        return temp_data

    def rounded_result(self):
        temp_dict = dict()

        """ 进行精度的转化 """
        for k_item, v_item in self.unit_changed_items().items():
            if k_item == "weight":
                if self.weight_rounding == "向上取整":
                    temp_dict[k_item] = Rounding.round_up(v_item, self.weight_precision)
                    print(temp_dict)
                elif self.weight_rounding == "向下取整":
                    temp_dict[k_item] = Rounding.round_down(v_item, self.weight_precision)
                else:
                    temp_dict[k_item] = Rounding.round_half_up(v_item, self.weight_precision)
            else:
                if self.size_rounding == "向上取整":
                    temp_dict[k_item] = Rounding.round_up(v_item, self.size_precision)

                elif self.size_rounding == "向下取整":
                    temp_dict[k_item] = Rounding.round_down(v_item, self.size_precision)
                else:
                    temp_dict[k_item] = Rounding.round_half_up(v_item, self.size_precision)

        """ 用转化后的数值，计算其围长，三边长，体积等 """
        tms_items = PackageCalcItems(**temp_dict)

        return {
            "单位_度转化完的原始数据": temp_dict,
            "重量": temp_dict.get("weight"),
            "最长边": tms_items.longest_side(),
            "次长边": tms_items.mid_side(),
            "最短边": tms_items.shortest_side(),
            "围长": tms_items.girth_origin(),
            "三边长": tms_items.perimeter_origin(),
            "两边长": tms_items.casual_two_sides_length(),
            "体积": tms_items.volume()
        }


if __name__ == '__main__':
    goods_info = {
        "weight": 12.22,
        "length": 13.32,
        "height": 13.32,
        "width": 113.48
    }
    result = CostPriceConversion(goods_info, "10", "20", "向上取整", 0.5, "向上取整", 0.1)
    print(result.rounded_result())
