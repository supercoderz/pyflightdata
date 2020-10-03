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

from .common_fr24 import *
from .flightdata import FlightData


def delay_rerun(*args):
    time.sleep(5)
    return True


@flaky(max_runs=5, rerun_filter=delay_rerun)
class TestCommonFR24(object):

    fr24 = FR24()

    def test_get_raw_flight_data_1(self):
        url = REG_BASE.format('vt-all', '', FlightData.AUTH_TOKEN, 1, 100)
        assert self.fr24.get_raw_flight_data(url).__len__() >= 0

    def test_get_raw_flight_data_2(self):
        url = FLT_BASE.format('vt-all', '', FlightData.AUTH_TOKEN, 1, 100)
        assert self.fr24.get_raw_flight_data(url).__len__() == 0

    def test_get_raw_flight_data_3(self):
        url = REG_BASE.format('ai101', '', FlightData.AUTH_TOKEN, 1, 100)
        assert self.fr24.get_raw_flight_data(url).__len__() == 0

    def test_get_raw_flight_data_4(self):
        url = FLT_BASE.format('ai101', '', FlightData.AUTH_TOKEN, 1, 100)
        assert self.fr24.get_raw_flight_data(url).__len__() >= 0

    def test_process_raw_flight_data_1(self):
        url = REG_BASE.format('vt-all', '', FlightData.AUTH_TOKEN, 1, 100)
        data = self.fr24.get_raw_flight_data(url)
        assert data.__len__() >= 0
        result = self.fr24.process_raw_flight_data(data)
        assert result.__len__() >= 0

    def test_get_data(self):
        url = REG_BASE.format('vt-all', '', FlightData.AUTH_TOKEN, 1, 100)
        assert self.fr24.get_data(url).__len__() >= 0

    def test_get_raw_country_data(self):
        assert self.fr24.get_raw_country_data().__len__() >= 0

    def test_process_raw_country_data(self):
        data = self.fr24.get_raw_country_data()
        assert data.__len__() >= 0
        result = self.fr24.process_raw_country_data(data)
        assert result.__len__() >= 0

    def test_get_raw_airport_data(self):
        assert self.fr24.get_raw_airport_data(
            AIRPORT_BASE + 'India').__len__() >= 0

    def test_process_raw_airport_data(self):
        data = self.fr24.get_raw_airport_data(AIRPORT_BASE + 'India')
        assert data.__len__() >= 0
        result = self.fr24.process_raw_airport_data(data)
        assert result.__len__() >= 0

    def test_get_aircraft_data(self):
        assert self.fr24.get_aircraft_data(REG_BASE.format(
            'VT-ALL', '', FlightData.AUTH_TOKEN, 1, 100)).__len__() >= 0

    def test_get_countries_data(self):
        assert self.fr24.get_countries_data().__len__() >= 0

    def test_get_airlines_data(self):
        assert self.fr24.get_airlines_data(REG_BASE).__len__() >= 0

    def test_get_raw_airlines_data(self):
        assert self.fr24.get_raw_airlines_data(REG_BASE).__len__() >= 0

    def test_process_raw_airlines_data(self):
        data = self.fr24.get_raw_airlines_data(REG_BASE)
        assert data.__len__() >= 0
        result = self.fr24.process_raw_airlines_data(data)
        assert result.__len__() >= 0

    def test_get_airline_fleet_data(self):
        assert self.fr24.get_airline_fleet_data(
            AIRLINE_FLEET_BASE.format('lufthansa-dlh'),False).__len__() >= 0

    def test_process_raw_airline_fleet_data(self):
        data = self.fr24.get_raw_airline_fleet_data(AIRLINE_FLEET_BASE.format(
            'lufthansa-dlh'))
        assert data.__len__() >= 0
        result = self.fr24.process_raw_airline_fleet_data(data, False)
        assert result.__len__() >= 0

    def test_get_airline_flight_data(self):
        assert self.fr24.get_airline_flight_data(
            AIRLINE_FLT_BASE.format('ai1', 100)).__len__() >= 0

    def test_get_airline_flight_data_points(self):
        assert self.fr24.get_airline_flight_data(
            AIRLINE_FLT_BASE_POINTS.format('SIN', 'HYD')).__len__() >= 0

    def test_get_airport_weather(self):
        data = self.fr24.get_airport_weather(
            AIRPORT_DATA_BASE.format('SIN', FlightData.AUTH_TOKEN, 1, 100))
        assert data.__len__() >= 0

    def test_get_airport_stats(self):
        data = self.fr24.get_airport_stats(
            AIRPORT_DATA_BASE.format('SIN', FlightData.AUTH_TOKEN, 1, 100))
        assert data.__len__() >= 0

    def test_get_airport_details(self):
        data = self.fr24.get_airport_details(
            AIRPORT_DATA_BASE.format('SIN', FlightData.AUTH_TOKEN, 1, 100))
        assert data.__len__() >= 0

    def test_get_airport_reviews(self):
        data = self.fr24.get_airport_reviews(
            AIRPORT_DATA_BASE.format('SIN', FlightData.AUTH_TOKEN, 1, 100))
        assert data.__len__() >= 0

    def test_get_airport_arrivals(self):
        data = self.fr24.get_airport_arrivals(
            AIRPORT_DATA_BASE.format('SIN', FlightData.AUTH_TOKEN, 1, 100))
        assert data.__len__() >= 0

    def test_get_airport_departures(self):
        data = self.fr24.get_airport_departures(
            AIRPORT_DATA_BASE.format('SIN', FlightData.AUTH_TOKEN, 1, 100))
        assert data.__len__() >= 0

    def test_get_airport_onground(self):
        data = self.fr24.get_airport_onground(
            AIRPORT_DATA_BASE.format('SIN', FlightData.AUTH_TOKEN, 1, 100))
        assert data.__len__() >= 0

    def test_get_raw_metars_hist(self):
        data = self.fr24.get_raw_metars_hist(
            AIRPORT_BASE.format('SIN') + "/weather")
        assert data.__len__() > 0

    def test_process_raw_metars_hist(self):
        data = self.fr24.get_raw_metars_hist(
            AIRPORT_BASE.format('SIN') + "/weather")
        data = self.fr24.process_raw_metars_hist(data)
        assert data.__len__() > 0

    def test_get_airport_metars_hist(self):
        data = self.fr24.get_airport_metars_hist(
            AIRPORT_BASE.format('SIN') + "/weather")
        assert data.__len__() > 0
