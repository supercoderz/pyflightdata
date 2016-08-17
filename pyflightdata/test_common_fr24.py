from .common_fr24 import *
from flaky import flaky

@flaky(max_runs=3)
class TestCommonFR24(object):

    def test_get_raw_flight_data_1(self):
        url = REG_BASE.format('vt-all')
        assert get_raw_flight_data(url).__len__() >= 0

    def test_get_raw_flight_data_2(self):
        url = FLT_BASE.format('vt-all')
        assert get_raw_flight_data(url).__len__() == 0

    def test_get_raw_flight_data_3(self):
        url = REG_BASE.format('ai101')
        assert get_raw_flight_data(url).__len__() == 0

    def test_get_raw_flight_data_4(self):
        url = FLT_BASE.format('ai101')
        assert get_raw_flight_data(url).__len__() >= 0

    def test_process_raw_flight_data_1(self):
        url = REG_BASE.format('vt-all')
        data = get_raw_flight_data(url)
        assert data.__len__() >= 0
        result = process_raw_flight_data(data)
        assert result.__len__() >= 0

    def test_get_data(self):
        url = REG_BASE.format('vt-all')
        assert get_data(url).__len__() >= 0

    def test_get_raw_country_data(self):
        assert get_raw_country_data().__len__() >= 0

    def test_process_raw_country_data(self):
        data = get_raw_country_data()
        assert data.__len__() >= 0
        result = process_raw_country_data(data)
        assert result.__len__() >= 0

    def test_get_raw_airport_data(self):
        assert get_raw_airport_data(AIRPORT_BASE + 'India').__len__() >= 0

    def test_process_raw_airport_data(self):
        data = get_raw_airport_data(AIRPORT_BASE + 'India')
        assert data.__len__() >= 0
        result = process_raw_airport_data(data)
        assert result.__len__() >= 0

    def test_get_raw_aircraft_image_data(self):
        assert get_raw_aircraft_image_data(REG_BASE.format('VT-ALL')).__len__() >= 0

    def test_process_raw_aircraft_image_data(self):
        data = get_raw_aircraft_image_data(REG_BASE.format('VT-ALL'))
        assert data.__len__() >= 0
        result = process_raw_aircraft_image_data(data)
        assert result.__len__() >= 0

    def test_get_raw_aircraft_image_data_dummy(self):
        assert get_raw_aircraft_image_data(REG_BASE.format('VT-A')).__len__() == 0

    def test_process_raw_aircraft_image_data_dummy(self):
        data = get_raw_aircraft_image_data(REG_BASE.format('VT-A'))
        assert data.__len__() == 0
        result = process_raw_aircraft_image_data(data)
        assert result.__len__() == 0

    def test_get_raw_aircraft_info_data(self):
        assert get_raw_aircraft_info_data(REG_BASE.format('VT-ALL')).__len__() >= 0

    def test_process_raw_aircraft_info_data(self):
        data = get_raw_aircraft_info_data(REG_BASE.format('VT-ALL'))
        assert data.__len__() >= 0
        result = process_raw_aircraft_info_data(data)
        assert result.__len__() >= 0

    def test_get_raw_aircraft_info_data_dummy(self):
        assert get_raw_aircraft_info_data(REG_BASE.format('VT-A')).__len__() == 0

    def test_process_raw_aircraft_info_data_dummy(self):
        data = get_raw_aircraft_info_data(REG_BASE.format('VT-A'))
        assert data.__len__() == 0
        result = process_raw_aircraft_info_data(data)
        assert result.__len__() == 0

    def test_get_aircraft_data(self):
        assert get_aircraft_data(REG_BASE.format('VT-ALL')).__len__() >= 0

    def test_get_countries_data(self):
        assert get_countries_data().__len__() >= 0

    def test_get_airlines_data(self):
        assert get_airlines_data(REG_BASE).__len__() >= 0

    def test_get_raw_airlines_data(self):
        assert get_raw_airlines_data(REG_BASE).__len__() >= 0

    def test_process_raw_airlines_data(self):
        data = get_raw_airlines_data(REG_BASE)
        assert data.__len__() >= 0
        result = process_raw_airlines_data(data)
        assert result.__len__() >= 0

    def test_get_airline_fleet_data(self):
        assert get_airline_fleet_data(
            REG_BASE.format('lufthansa-dlh')).__len__() >= 0

    def test_get_raw_airline_fleet_data(self):
        assert get_raw_airline_fleet_data(
            REG_BASE.format('lufthansa-dlh')).__len__() >= 0

    def test_process_raw_airline_fleet_data(self):
        data = get_raw_airline_fleet_data(REG_BASE.format('lufthansa-dlh'))
        assert data.__len__() >= 0
        result = process_raw_airline_fleet_data(data)
        assert result.__len__() >= 0

    def test_get_airline_flight_data(self):
        assert get_airline_flight_data(
            FLT_BASE.format('air-india-aic')).__len__() >= 0

    def test_get_raw_airline_flight_data(self):
        assert get_raw_airline_flight_data(
            FLT_BASE.format('air-india-aic')).__len__() >= 0

    def test_process_raw_airline_flight_data(self):
        data = get_raw_airline_flight_data(FLT_BASE.format('air-india-aic'))
        assert data.__len__() >= 0
        result = process_raw_airline_flight_data(data)
        assert result.__len__() >= 0
