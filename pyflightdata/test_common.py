from .common import *
from .common_fr24 import FLT_BASE


class TestCommon(object):

    def test_get_page_or_none_1(self):
        assert get_page_or_none('http://google.com/abcd') is None

    def test_get_page_or_none_2(self):
        assert get_page_or_none('http://www.flightradar24.com/') is not None

    def test_get_soup_or_none_1(self):
        assert get_soup_or_none(None) is None

    def test_get_soup_or_none_2(self):
        assert get_soup_or_none('http://www.flightradar24.com/') is not None

    def test_get_raw_data(self):
        url = FLT_BASE + 'ai101'
        assert get_raw_data(url, 'tblFlightData', 'tr').__len__() > 0

    def test_encode_and_get(self):
        assert encode_and_get('test') is not None
