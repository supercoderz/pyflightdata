from .common import *

REG_BASE = 'https://www.flightradar24.com/data/airplanes/'
FLT_BASE = 'http://www.flightradar24.com/data/flights/'
AIRPORT_BASE = 'http://www.flightradar24.com/data/airports/'

#Handle all the flights data		
def get_raw_flight_data(url):
	return get_raw_data(url,'tblFlightData','tr')[1:]

def get_entry_details(entry,by_tail=False):
	details = {}
	cols = entry.find_all('td')
	if cols.__len__() > 1:
		details['date'] = cols[0].text
		details['from'] = cols[1].text
		details['to'] = cols[2].text
		if by_tail :
			details['flight'] = cols[3].text
		else:
			details['aircraft'] = cols[3].text
		details['std'] = cols[4].text
		details['atd'] = cols[5].text
		details['sta'] = cols[6].text
		details['status'] = cols[7].text
	return details

def merge(attrs,details):
	attrs.update(details)
	return attrs

def process_raw_flight_data(data,by_tail=False):
	result = []
	for entry in data:
		attrs = entry.attrs
		data = get_entry_details(entry,by_tail)
		d = merge(attrs,data)
		if d.__len__()>0:
			result.append(d)
	return result

def get_data(url,by_tail=False):
	data = get_raw_flight_data(url)
	result = process_raw_flight_data(data,by_tail)
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
	

#handle aircraft information
def get_aircraft_data(url):
	img_data = get_raw_aircraft_image_data(url)
	result = process_raw_aircraft_image_data(img_data)
	info_data = get_raw_aircraft_info_data(url)
	result.update(process_raw_aircraft_info_data(info_data))
	return result

def get_raw_aircraft_image_data(url):
	return get_raw_data(url,'cntAircraftData','img')

def get_raw_aircraft_info_data(url):
	return get_raw_data(url,'cntAircraftData','dl')

def process_raw_aircraft_image_data(data):
	result = {}
	try:
		image_urls = []
		for image in data:
			url = image.attrs['src']
			image_urls.append(url)
		if image_urls.__len__()>0:
			result['images']=image_urls
	except:
		pass
	return result

def process_raw_aircraft_info_data(data):
	result = {}
	try:
		elements = data[0].findAll()
		result['ModeS'] = elements[1].text
		result['Registration'] = elements[3].text
		result['Type code'] = elements[5].text
		result['Type'] = elements[7].text
		result['S/N'] = elements[9].text
		result['Airline'] = elements[11].text
	except:
		pass
	return result