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
				#ignore the header
				return soup.find(id='tblFlightData').find_all('tr')[1:]
			except:
				return []
		else:
			return []
	else:
		return []
		
def get_entry_details(entry):
	details = {}
	cols = entry.find_all('td')
	if cols.__len__() > 1:
		details['date'] = cols[0].text
		details['from'] = cols[1].text
		details['to'] = cols[2].text
		details['aircraft'] = cols[3].text
		details['std'] = cols[4].text
		details['atd'] = cols[5].text
		details['sta'] = cols[6].text
		details['status'] = cols[7].text
	return details

def merge(attrs,details):
	attrs.update(details)
	return attrs

def process_raw_flight_data(data):
	result = []
	for entry in data:
		attrs = entry.attrs
		data = get_entry_details(entry)
		d = merge(attrs,data)
		if d.__len__()>0:
			result.append(d)
	return result

def get_data(url):
	data = get_raw_flight_data(url)
	result = process_raw_flight_data(data)
	return result