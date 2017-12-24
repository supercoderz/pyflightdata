from .flightdata import FlightData
from flaky import flaky
import time

def delay_rerun(*args):
    time.sleep(5)
    return True

f=FlightData()

@flaky(max_runs=5,rerun_filter=delay_rerun)
class TestGetByFlightNumber(object):

    def test_simple_get(self):
        f.get_history_by_flight_number('AI101')

    def test_check_there_is_history_data(self):
        result = f.get_history_by_flight_number('AI101')
        assert result.__len__() > 0

@flaky(max_runs=5,rerun_filter=delay_rerun)
class TestGetByTailNumber(object):

    def test_simple_get(self):
        f.get_history_by_tail_number('VT-ALL')

    def test_check_there_is_history_data(self):
        result = f.get_history_by_tail_number('9V-SMC')
        assert result.__len__() > 0

    def test_aircraft_info(self):
        result = f.get_info_by_tail_number('VT-ALL')
        assert result.__len__() > 0

@flaky(max_runs=5,rerun_filter=delay_rerun)
class TestOtherFeatures(object):

    def test_get_countries(self):
        assert f.get_countries().__len__() > 0

    def test_get_airports(self):
        assert f.get_airports('India').__len__() > 0

    def test_get_airlines(self):
        assert f.get_airlines().__len__() > 0

    def test_get_fleet(self):
        assert f.get_fleet('air-india-aic').__len__() >= 0

    def test_get_fleet(self):
        assert f.get_flights('air-india-aic').__len__() >= 0
