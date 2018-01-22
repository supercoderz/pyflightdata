import time

from flaky import flaky

from .common import ProcessorMixin
from .common_fr24 import AIRPORT_BASE, FLT_BASE
from .flightdata import FlightData


def delay_rerun(*args):
    time.sleep(5)
    return True


class TestProcessor(ProcessorMixin):
    pass


@flaky(max_runs=5, rerun_filter=delay_rerun)
class TestCommon(object):

    tp = TestProcessor()

    def test_get_page_or_none_1(self):
        assert self.tp.get_page_or_none('http://google.com/abcd') is None

    def test_get_page_or_none_2(self):
        assert self.tp.get_page_or_none(
            'http://www.flightradar24.com/') is not None

    def test_get_soup_or_none_1(self):
        assert self.tp.get_soup_or_none(None) is None

    def test_get_raw_data_json(self):
        url = FLT_BASE.format('AI101', FlightData.AUTH_TOKEN, 1, 100)
        assert self.tp.get_raw_data_json(
            url, 'result.response.data').__len__() > 0

    def test_encode_and_get(self):
        assert self.tp.encode_and_get('test') is not None

    def test_traverse(self):
        assert self.tp.get_raw_data(
            AIRPORT_BASE, 'tbl-datatable', 'tbody', 'tr').__len__() > 0
