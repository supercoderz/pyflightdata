import time

from flaky import flaky

from .flightdata import FlightData


def delay_rerun(*args):
    time.sleep(5)
    return True


f = FlightData()


@flaky(max_runs=5, rerun_filter=delay_rerun)
class TestGetByFlightNumber(object):

    def test_simple_get(self):
        f.get_history_by_flight_number('AI101')

    def test_check_there_is_history_data(self):
        result = f.get_history_by_flight_number('AI101')
        assert result.__len__() > 0


@flaky(max_runs=5, rerun_filter=delay_rerun)
class TestGetByTailNumber(object):

    def test_simple_get(self):
        f.get_history_by_tail_number('VT-ALL')

    def test_check_there_is_history_data(self):
        result = f.get_history_by_tail_number('9V-SMC')
        assert result.__len__() > 0

    def test_aircraft_info(self):
        result = f.get_info_by_tail_number('VT-ALL')
        assert result.__len__() > 0

    def test_aircraft_images(self):
        result = f.get_images_by_tail_number('VT-ALL')
        assert result.__len__() > 0


@flaky(max_runs=5, rerun_filter=delay_rerun)
class TestOtherFeatures(object):

    def test_get_countries(self):
        assert f.get_countries().__len__() > 0

    def test_get_airports(self):
        assert f.get_airports('India').__len__() > 0

    def test_get_airlines(self):
        assert f.get_airlines().__len__() > 0

    def test_get_fleet(self):
        assert f.get_fleet('air-india-aic').__len__() >= 0

    def test_get_flights(self):
        assert f.get_flights('air-india-aic').__len__() >= 0

    def test_get_airport_weather(self):
        d = f.get_airport_weather('SIN')
        assert d.__len__() >= 0
        if d['sky']['visibility']['mi'] != 'None':
            assert (d['sky']['visibility']['km'] ==
                    d['sky']['visibility']['mi'] * 1.6094)

    def test_get_airport_metars(self):
        assert f.get_airport_metars('SIN') is not None

    def test_get_airport_metars_hist(self):
        assert f.get_airport_metars_hist('SIN').__len__() > 0

    def test_get_airport_stats(self):
        assert f.get_airport_stats('SIN').__len__() >= 0

    def test_get_airport_details(self):
        d = f.get_airport_details('SIN')
        assert d.__len__() >= 0
        assert type(d['position']['elevation']) == dict
        assert d['position']['elevation']['ft'] != None
        assert d['position']['elevation']['m'] != None

    def test_get_airport_reviews(self):
        assert f.get_airport_reviews('SIN').__len__() >= 0

    def test_get_airport_arrivals(self):
        assert f.get_airport_arrivals('SIN').__len__() >= 0

    def test_get_airport_departures(self):
        assert f.get_airport_departures('SIN').__len__() >= 0

    def test_get_airport_onground(self):
        assert f.get_airport_onground('SIN').__len__() >= 0

    def test_not_logged_in(self):
        assert f.is_authenticated() == False

    def test_decode_metar(self):
        assert f.decode_metar(
            "WSSS 181030Z 04009KT 010V080 9999 FEW018TCU BKN300 29/22 Q1007 NOSIG") is not None
