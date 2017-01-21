from .common import *
from .common_fr24 import FLT_BASE,AIRPORT_BASE
from flaky import flaky

@flaky(max_runs=5)
class TestCommon(object):

    def test_get_page_or_none_1(self):
        assert get_page_or_none('http://google.com/abcd') is None

    def test_get_page_or_none_2(self):
        assert get_page_or_none('http://www.flightradar24.com/') is not None

    def test_get_soup_or_none_1(self):
        assert get_soup_or_none(None) is None

    def test_get_soup_or_none_2(self):
        assert get_soup_or_none('http://www.flightradar24.com/') is not None

    def test_get_raw_data_json(self):
        url = FLT_BASE.format('ek7')
        assert get_raw_data_json(url, 'result.response.data').__len__() > 0

    def test_encode_and_get(self):
        assert encode_and_get('test') is not None
        
    def test_traverse(self):
        assert get_raw_data(AIRPORT_BASE, 'tbl-datatable', 'tbody','tr').__len__() > 0
