import requests
from bs4 import BeautifulSoup

REG_BASE = 'http://www.flightradar24.com/data/airplanes/'
FLT_BASE = 'http://www.flightradar24.com/data/flights/'

def get_page_or_none(url):
	result = requests.get(url)
	if result.status_code == 200:
		return result.content
	else:
		return None

def get_soup_or_none(content):
	try:
		soup = BeautifulSoup(content)
		return soup
	except:
		return None
		
def get_raw_flight_data(url):
	content = get_page_or_none(url)
	if content:
		soup = get_soup_or_none(content)
		if soup:
			try:
				return soup.find(id='tblFlightData').find_all('tr')
			except:
				return []
		else:
			return []
	else:
		return []