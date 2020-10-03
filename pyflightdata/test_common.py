# MIT License
#
# Copyright (c) 2020 Hari Allamraju
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time

from flaky import flaky

from .common import ProcessorMixin
from .common_fr24 import AIRPORT_BASE, FLT_BASE
from .flightdata import FlightData
from .utils import *


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
        url = FLT_BASE.format('AI101', FlightData.AUTH_TOKEN, 1, 100, nowtimestamp_millis())
        assert self.tp.get_raw_data_json(
            url, 'result.response.data').__len__() > 0

    def test_encode_and_get(self):
        assert self.tp.encode_and_get('test') is not None

    def test_traverse(self):
        assert self.tp.get_raw_data(
            AIRPORT_BASE.format('India'), 'tbl-datatable', 'tbody', 'tr','td','a').__len__() > 0
