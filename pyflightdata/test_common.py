from .common import *

class TestCommon(object):
	
	def test_get_page_or_none_1(self):
		assert get_page_or_none('http://google.com/abcd') == None
	
	def test_get_page_or_none_2(self):
		assert get_page_or_none('http://www.flightradar24.com/') is not None
		
	def test_get_soup_or_none_1(self):
		assert get_soup_or_none(None) == None
		
	def test_get_soup_or_none_2(self):
		assert get_soup_or_none('http://www.flightradar24.com/') is not None
		
	def test_get_raw_flight_data_1(self):
		url = REG_BASE+'vt-all'
		assert get_raw_flight_data(url).__len__() > 0
		
	def test_get_raw_flight_data_2(self):
		url = FLT_BASE+'vt-all'
		assert get_raw_flight_data(url).__len__() == 0		

	def test_get_raw_flight_data_3(self):
		url = REG_BASE+'ai101'
		#thisis to account for how the site responds at the moment; might change later
		assert get_raw_flight_data(url).__len__() == 3
		
	def test_get_raw_flight_data_4(self):
		url = FLT_BASE+'ai101'
		assert get_raw_flight_data(url).__len__() > 0		