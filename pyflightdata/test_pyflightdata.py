from .flightdata import *

class TestGetByFlightNumber(object):
	
	def test_simple_get(self):
		get_history_by_flight_number('AI101')
		
	def test_check_there_is_history_data(self):
		result = get_history_by_flight_number('AI101')
		assert result.__len__()>0

class TestGetByTailNumber(object):
	
	def test_simple_get(self):
		get_history_by_tail_number('VT-ALL')
		
	def test_check_there_is_history_data(self):
		result = get_history_by_tail_number('VT-ALL')
		assert result.__len__()>0

	def test_aircraft_info(self):
		result = get_info_by_tail_number('VT-ALL')
		assert result.__len__()>0

class TestCountriesAndAirports(object):
	
	def test_get_countries(self):
		assert get_countries().__len__()>0
	
	def test_get_airports(self):
		assert get_airports('India').__len__()>0
	