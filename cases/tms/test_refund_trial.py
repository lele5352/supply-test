"""
测试客退试算
"""

import pytest
import allure
from cases import homary_tms
from config.third_party_api_configs.tms_api_config import TransportType

# GLS 测试渠道
gls_trial_data = (
    # 仓库地址id，渠道id
    (170, 77),
)


@allure.feature("测试模块：客退试算-快递")
class TestExpressTrial:
    @allure.story('测试场景：快递试算，使用US地址，预期成功')
    @pytest.mark.parametrize("warehouse_address, channel_id", gls_trial_data)
    def test_us_express_trial(self, warehouse_address, channel_id):

        with allure.step("组织试算参数"):
            req = homary_tms.build_trial_body(
                TransportType.EXPRESS.value,
                warehouse_address,
                'US',
                channel_id=channel_id
            )

        with allure.step("执行试算"):
            trial_result = homary_tms.do_trial(req)

            assert trial_result.get('code', 500) == 200, "断言 http status=200 失败"

    @allure.story('测试场景：快递试算，使用FR地址，预期失败（配送区域不可达）')
    @pytest.mark.parametrize("warehouse_address, channel_id", gls_trial_data)
    def test_trial_fail_reach(self, warehouse_address, channel_id):

        with allure.step("组织试算参数"):
            req = homary_tms.build_trial_body(
                TransportType.EXPRESS.value,
                warehouse_address,
                'FR',
                channel_id=channel_id
            )

        with allure.step("执行试算"):
            trial_result = homary_tms.do_trial(req)

            assert trial_result.get('message') == '无可用渠道', "断言 配送区域不可达 失败"

    @allure.story('测试场景：快递试算，使用US地址，预期失败（限制规则不可发）')
    @pytest.mark.parametrize("warehouse_address, channel_id", gls_trial_data)
    def test_trial_fail_limit(self, warehouse_address, channel_id):

        with allure.step("组织试算参数"):
            req = homary_tms.build_trial_body(
                TransportType.EXPRESS.value,
                warehouse_address,
                'US',
                channel_id=channel_id,
                weight=21
            )

        with allure.step("执行试算"):
            trial_result = homary_tms.do_trial(req)

            assert trial_result.get('message') == '无可用渠道', "断言 限制规则不可发 失败"

    @allure.story('测试场景：快递试算，本地成本价计算')
    @pytest.mark.parametrize("warehouse_address, channel_id", gls_trial_data)
    def test_trial_fee(self, warehouse_address, channel_id):

        weight = 10

        with allure.step("组织试算参数"):
            req = homary_tms.build_trial_body(
                TransportType.EXPRESS.value,
                warehouse_address,
                'US',
                channel_id=channel_id,
                weight=weight
            )

        with allure.step("执行试算"):
            trial_result = homary_tms.do_trial(req)
            assert trial_result.get('code', 500) == 200, "断言 http status=200 失败"

        with allure.step("成本价计算结果检查（使用成本价规则id：111）"):

            尾程其他杂费 = 5.00
            尾程基础运费 = 10.00
            尾程超重量附加费 = round(1.5 * weight, 2)

            try:
                logistics_prices = trial_result["data"]["expressPrices"]["dividedPackageSolution"][0]["logisticsPrices"]
            except KeyError:
                assert False, "获取费用项列表失败"

            fee_map = {}
            for item in logistics_prices[0]["feeItems"]:
                fee_map[item["feeItemName"]] = item["saleAmount"]

            assert float(fee_map["尾程其他杂费"]) == pytest.approx(尾程其他杂费, rel=0.01), "费用项价格断言失败"
            assert float(fee_map["尾程基础运费"]) == pytest.approx(尾程基础运费, rel=0.01), "费用项价格断言失败"
            assert float(fee_map["尾程超重量附加费"]) == pytest.approx(尾程超重量附加费, rel=0.01), "费用项价格断言失败"


