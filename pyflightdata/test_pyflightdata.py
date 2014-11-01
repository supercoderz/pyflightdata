from .flightdata import get_by_flight_number, get_by_tail_number, get_countries, get_airports

class TestGetByFlightNumber(object):
	
	def test_simple_get(self):
		get_by_flight_number('AI101')
		
	def test_check_there_is_data(self):
		result = get_by_flight_number('AI101')
		assert result.__len__()>0

class TestGetByTailNumber(object):
	
	def test_simple_get(self):
		get_by_tail_number('VT-ALL')
		
	def test_check_there_is_data(self):
		result = get_by_tail_number('VT-ALL')
		assert result.__len__()>0

class TestCountriesAndAirports(object):
	def test_get_countries(self):
		assert get_countries().__len__()>0
	
	def test_get_airports(self):
		assert get_airports('India').__len__()>0
	