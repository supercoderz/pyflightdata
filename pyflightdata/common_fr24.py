import requests
from bs4 import BeautifulSoup

REG_BASE = 'http://www.flightradar24.com/data/airplanes/'
FLT_BASE = 'http://www.flightradar24.com/data/flights/'
AIRPORT_BASE = 'http://www.flightradar24.com/data/airports/'

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

def get_raw_data(url,item,element):
	content = get_page_or_none(url)
	if content:
		soup = get_soup_or_none(content)
		if soup:
			try:
				#ignore the header
				return soup.find(id=item).find_all(element)
			except:
				return []
		else:
			return []
	else:
		return []


#Handle all the flights data		
def get_raw_flight_data(url):
	return get_raw_data(url,'tblFlightData','tr')[1:]

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

#Handle getting countries	
def get_raw_country_data():
	return get_raw_data(AIRPORT_BASE,'countriesList','li')

def process_raw_country_data(data):
	result = []
	for entry in data:
		result.append(entry.attrs['data-name'].strip())
	return result

def get_countries_data():
	data = get_raw_country_data()
	result = process_raw_country_data(data)
	return result
	
#Handle getting the airports in a country
def get_raw_airport_data(url):
	return get_raw_data(url,'airlineList','li')

def process_raw_airport_data(data):
	result = []
	for entry in data:
		name = entry.find('div').text.strip()
		code = entry.find('div').find('a').attrs['href'].split('/')[-1]
		result.append((name,code))
	return result

def get_airports_data(url):
	data = get_raw_airport_data(url)
	result = process_raw_airport_data(data)
	return result
	
