from functools import reduce
from utils.rounding_handler import *
from utils.unit_change_handler import UnitChange as UC


class PackageCalcItems:
    """获取包裹维度的各项维度数据，需要传入包裹维度的长、宽、高、实重；单件sku维度的最大实重、最小实重、最大长度、最小长度；原单位、目标单位
    :param int length: 包裹的长
    :param int width: 包裹的宽
    :param int height: 包裹的高
    :param int weight: 包裹的总重量
    :param list sku_list: 包裹里面的sku信息
    :param int good_unit: 包裹属性的原单位，10-国际，20-英制
    :param int ch_unit: 包裹属性换算的目标单位，10-国际，20-英制
    :param dict calc_config: 换算的配置，包含尺寸取整方式和精度，重量取整方式和精度渠道
    :param int volume_precision: 体积系数
    """

    def __init__(self, length, width, height, weight, sku_list, good_unit, ch_unit, calc_config, volume_precision):
        self.source_unit = good_unit
        self.target_unit = ch_unit
        self.weight = weight
        self.length = length
        self.width = width
        self.height = height
        self.sku_list = sku_list
        self.weight_rounding = calc_config.get("weightRoundMode")
        self.weight_precision = calc_config.get("weightRoundAccuracy")
        self.size_rounding = calc_config.get("dimensionRoundMode")
        self.size_precision = calc_config.get("dimensionRoundAccuracy")
        self.volume_precision = volume_precision

    @staticmethod
    def calc_item(num, num_type, round_mode, round_precision, source_unit, target_unit):
        unit_change_num = UC.change(num, num_type, source_unit, target_unit)
        return Rounding.do_round(round_mode, unit_change_num, round_precision)

    def pkg_side_lengths(self):
        return [
            self.calc_item(length, "size", self.size_rounding, self.size_precision, self.source_unit, self.target_unit)
            for length in (self.length, self.width, self.height)]

    def pkg_weight(self):
        return self.calc_item(self.weight, "weight", self.weight_rounding, self.weight_precision, self.source_unit,
                              self.target_unit)

    def pkg_longest_side(self):
        """最长边"""
        return max(self.pkg_side_lengths())

    def pkg_mid_side(self):
        """第二长边"""
        return sorted(self.pkg_side_lengths(), reverse=True)[1]

    def pkg_shortest_side(self):
        """最短边"""
        return min(self.pkg_side_lengths())

    def pkg_girth(self):
        """围长"""
        girth = self.pkg_side_lengths()[0] + (self.pkg_side_lengths()[1] + self.pkg_side_lengths()[2]) * 2
        return Rounding.do_round(self.size_rounding, round(girth, 6), self.size_precision)

    def girth_origin(self):
        """围长,原始的 长+(宽+高)×2"""
        return self.length + (self.width + self.height) * 2

    def perimeter_origin(self):
        """三边长，原始长度  """
        return round(self.length + self.width + self.height, 6)

    def pkg_two_side_lengths(self):
        """任意两边长：长+宽"""
        len_and_width = self.pkg_side_lengths()[0] + self.pkg_side_lengths()[1]
        len_and_height = self.pkg_side_lengths()[0] + self.pkg_side_lengths()[2]
        width_and_height = self.pkg_side_lengths()[1] + self.pkg_side_lengths()[2]
        two_side_lengths = [
            Rounding.do_round(self.size_rounding, round(len_and_width, 6), self.size_precision),
            Rounding.do_round(self.size_rounding, round(len_and_height, 6), self.size_precision),
            Rounding.do_round(self.size_rounding, round(width_and_height, 6), self.size_precision)
        ]
        two_side_lengths.sort(reverse=True)
        return two_side_lengths

    def casual_two_sides_length(self):
        """任意两边长，长+宽；长+高；宽+高"""
        return {"长+宽": self.pkg_length() + self.pkg_width(), "长+高": self.pkg_length() + self.pkg_height(),
                "高+宽": self.pkg_width() + self.pkg_height()}

    def pkg_perimeter(self):
        """周长"""
        perimeter = sum(self.pkg_side_lengths())
        return Rounding.do_round(self.size_rounding, round(perimeter, 6), self.size_precision)

    def pkg_volume(self):
        """体积=长*宽*高"""
        volume = reduce(lambda x, y: x * y, self.pkg_side_lengths())
        return Rounding.do_round(self.size_rounding, round(volume, 6), self.size_precision)

    def pkg_volume_weight(self):
        """体积=长*宽*高"""
        volume = self.pkg_volume()
        volume_weight = volume / self.volume_precision
        return Rounding.do_round(self.weight_rounding, round(volume_weight, 6), self.weight_precision)

    def pkg_bill_weight(self):
        return max(self.pkg_weight(), self.pkg_volume_weight())

    def pkg_sku_item_list(self, ):
        temp_list = list()
        temp_list.extend(
            [{
                "skuMaxLength": self.calc_item(sku["skuMaxLength"], "size", self.size_rounding, self.size_precision,
                                               self.source_unit, self.target_unit),
                "skuWeight": self.calc_item(sku["skuWeight"], "weight", self.weight_rounding, self.weight_precision,
                                            self.source_unit, self.target_unit)

            } for sku in self.sku_list]
        )
        return temp_list

    def tray_density(self):
        """美卡托盘密度"""
        if self.source_unit == 10:
            # 判断是否需要换算单位，若货物信息的单位为国际单位，则需要换算，传True
            weight = UC.change(self.weight, "weight", 10, 20)
            volume = UC.change(self.length * self.width * self.height, "volume", 10, 20)
            density = weight / volume * 1728
            return round(density, 2)
        return round(self.weight / self.length * self.width * self.height * 1728, 10)

    def package_items(self):
        return {
            "weight": self.pkg_weight(),
            "volumeWeight": self.pkg_volume_weight(),
            "billWeight": self.pkg_bill_weight(),
            "longestEdge": self.pkg_longest_side(),
            "secondSide": self.pkg_mid_side(),
            "shortestEdge": self.pkg_shortest_side(),
            "girth": self.pkg_girth(),
            "perimeter": self.pkg_perimeter(),
            "maxSideLength": max(self.pkg_two_side_lengths()),
            "midSideLength": self.pkg_two_side_lengths()[1],
            "minSideLength": min(self.pkg_two_side_lengths()),
            "volume": self.pkg_volume(),
            "length": self.pkg_side_lengths()[0],
            "width": self.pkg_side_lengths()[1],
            "height": self.pkg_side_lengths()[2],
            "skus": self.pkg_sku_item_list()
        }


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
