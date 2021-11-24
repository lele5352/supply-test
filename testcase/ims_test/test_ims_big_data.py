import time
import pytest
from controller import ims, wms


class TestImsBigData():
    def setup_class(self):
        self.ware_skus = ['68718842205A01', '25297066062A01', '58794200526A01', '17067658035A01', '76972538042A01',
                          '46343526649A01', '64337019363A01', '24935910361A01', '58794200075A01', '58794200675A01',
                          '17067658171A01', '32090972682A01', '28265130766A01', '65502337968A01', '44597691661A01',
                          '68718842326A01', '68718842583A01', '24935910793A01', '70316221956A01', '30756027844A01',
                          '28265130607A01', '65502337092A01', '65502337459A01', '46343526431A01', '64337019734A01',
                          '44597691629A01', '76972538839A01', '70316221265A01', '20622209350A01', '70316221939A01',
                          '30756027335A01', '28265130164A01', '46343526407A01', '44597691959A01', '24935910257A01',
                          '25297066635A01', '20622209671A01', '65502337983A01', '44597691262A01', '68718842440A01',
                          '17067658866A01', '17067658232A01', '20622209269A01', '70316221690A01', '30756027917A01',
                          '28265130523A01', '30756027669A01', '28265130025A01', '46343526917A01', '70316221338A01',
                          '23269605035A01', '79040408670A01', '76972538641A01', '31139935337A01', '31139935327A01',
                          '49867082046A01', '31139935463A01', '85184738999A01', '40991362111A01', '40991362981A01',
                          '34185049209A01', '21572453098A01', '76972538862A01', '31139935741A01', '69263633765A01',
                          '85184738265A01', '34185049176A01', '82647990661A01', '59276388841A01', '27180292331A01',
                          '21572453161A01', '69667132849A01', '58098403395A01', '31139935260A01', '49867082855A01',
                          '87549937272A01', '87258557166A01', '27180292795A01', '13165789781A01', '31139935937A01',
                          '49867082543A01', '95241686939A01', '85828995629A01', '85828995557A01', '58098403028A01',
                          '21572453013A01', '20622209014A01', '31139935517A01', '31139935548A01', '31139935269A01',
                          '95241686427A01', '34185049648A01', '87682034011A01', '23269605815A01', '23269605272A01',
                          '18546799244A01', '59276388680A01', '39513819707A01', '30630549089A01', '30630549926A01']
        self.ims = ims
        self.wms = wms
        self.sj_location_id = self.wms.get_location_id(self.wms.get_location_codes(1, 5, 513)[0], 513)

    @pytest.mark.skip(reason='test')
    def test_other_into_warehouse(self):
        ware_sku_list = list()
        for ware_sku in self.ware_skus:
            ware_sku_list.append(
                {
                    "qty": 1,
                    "storageLocationId": self.sj_location_id,
                    "storageLocationType": 5,
                    "wareSkuCode": ware_sku
                }
            )
        start_time = int(time.time() * 1000)
        res = ims.other_into_warehouse(ware_sku_list, 513, 513)
        end_time = int(time.time() * 1000)
        print("total seconds:%s" % (end_time - start_time))
        assert res['code'] == 200
        assert end_time - start_time < 5000

    def test_other_out_warehouse_block(self):
        ware_sku_list = list()
        for ware_sku in self.ware_skus:
            ware_sku_list.append(
                {
                    "qty": 1,
                    "storageLocationId": self.sj_location_id,
                    "storageLocationType": 5,
                    "wareSkuCode": ware_sku
                }
            )
        start_time = int(time.time() * 1000)
        res = ims.qualified_goods_other_out_block(ware_sku_list, 513, 513)
        end_time = int(time.time() * 1000)
        print("total seconds:%s" % (end_time - start_time))
        assert res['code'] == 200
        assert end_time - start_time < 5000


if __name__ == '__main__':
    pytest.main()
