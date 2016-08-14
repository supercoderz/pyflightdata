from .common import *

ROOT = 'http://www.flightradar24.com'
REG_BASE = 'https://api.flightradar24.com/common/v1/flight/list.json?query={0}&fetchBy=reg&page=1&limit=100'
FLT_BASE = 'https://api.flightradar24.com/common/v1/flight/list.json?query={0}&fetchBy=flight&page=1&limit=100'
AIRPORT_BASE = 'http://www.flightradar24.com/data/airports/'
AIRLINE_BASE = 'https://www.flightradar24.com/data/aircraft/'
AIRLINE_FLT_BASE = 'https://www.flightradar24.com/data/flights/{0}'

# Handle all the flights data


def get_raw_flight_data(url):
    data = get_raw_data_json(url, 'result.response.data')
    if data:
        return data[0] or []
    return []

def process_raw_flight_data(data, by_tail=False):
    #TODO fix later
    return data


def get_data(url, by_tail=False):
    data = get_raw_flight_data(url)
    result = process_raw_flight_data(data, by_tail)
    return result

# Handle getting countries


def get_raw_country_data():
    return get_raw_data(AIRPORT_BASE, 'tbl-datatable', 'tbody','tr') or []


def process_raw_country_data(data):
    result = []
    for entry in data:
        cells = entry.find_all('td')
        if cells:
            #this will break one day
            for cell in cells[1:2]:
                link = cell.find('a')
                if link:
                    if 'data-country' in link.attrs:
                        record={}
                        for attr in link.attrs:
                            if attr not in ['href','class','onclick']:
                                attr_new = attr.replace('data-','')
                                record[attr_new] = link[attr]
                        images = link.find_all('img')
                        if images:
                            for image in images:
                                record['img'] = image['bn-lazy-src']
                        result.append(record)
    return result


def get_countries_data():
    data = get_raw_country_data()
    result = process_raw_country_data(data)
    return result

# Handle getting the airports in a country


def get_raw_airport_data(url):
    return get_raw_data(url, 'tbl-datatable', 'tbody','tr') or []


def process_raw_airport_data(data):
    result = []
    for entry in data:
        cells = entry.find_all('td')
        if cells:
            for cell in cells:
                link = cell.find('a')
                if link:
                    record = {}
                    for attr in link.attrs:
                        if attr not in ['href','class','onclick']:
                            attr_new = attr.replace('data-','')
                            record[attr_new] = link[attr]
                    result.append(record)
    return result


def get_airports_data(url):
    data = get_raw_airport_data(url)
    result = process_raw_airport_data(data)
    return result


# handle aircraft information
def get_aircraft_data(url):
    img_data = get_raw_aircraft_image_data(url)
    result = process_raw_aircraft_image_data(img_data)
    info_data = get_raw_aircraft_info_data(url)
    result.update(process_raw_aircraft_info_data(info_data))
    return result


def get_raw_aircraft_image_data(url):
    return get_raw_data(url, 'cntAircraftData', 'img') or []


def get_raw_aircraft_info_data(url):
    return get_raw_data(url, 'cntAircraftData', 'dl') or []


def process_raw_aircraft_image_data(data):
    result = {}
    try:
        image_urls = []
        for image in data:
            url = image.attrs['src']
            image_urls.append(url)
        if image_urls.__len__() > 0:
            result['images'] = image_urls
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

# Handle getting all the airlines


def get_raw_airlines_data(url):
    return get_raw_data(url, 'tbl-datatable', 'tbody', 'tr') or []


def process_raw_airlines_data(data):
    result = []
    for entry in data:
        cells = entry.find_all('td')
        if cells:
            for cell in cells:
                link = cell.find('a')
                if link:
                    if 'data-country' in link.attrs:
                        record = {}
                        for attr in link.attrs:
                            if attr not in ['href','class','onclick','target']:
                                attr_new = attr.replace('data-','')
                                record[attr_new] = link[attr]
                        span = link.find('span')
                        if span:
                            images = span.find_all('img')
                            if images:
                                for image in images:
                                    record['img'] = image['bn-lazy-src']
                        result.append(record)
    return result


def get_airlines_data(url):
    data = get_raw_airlines_data(url)
    result = process_raw_airlines_data(data)
    return result

# Handle getting the fleet


def get_raw_airline_fleet_data(url):
    slide =  get_raw_data_class(url, 'horizontal-slide')
    return slide.find_all('li',class_='parent') if slide else []

def process_raw_airline_fleet_data(data):
    result = []
    for parent in data:
        record = {}
        div = parent.find('div')
        if div:
            #yeah this sucks
            div = div.find('div')
            if div:
                atype = encode_and_get(div.text.strip())
                atype = atype[0:atype.index('\\t')]
                record['aircraft-type'] = atype
                span = div.find('span')
                if span:
                    record['count']=encode_and_get(span.text.strip())
        ul = parent.find('ul')
        if ul:
            regs = ul.find_all('li')
            if regs:
                reg_list = []
                for reg in regs:
                    link = reg.find('a')
                    if link:
                        reg_list.append(encode_and_get(link.text.strip()))
                record['aircraft-regs'] = reg_list
        result.append(record)
    return result


def get_airline_fleet_data(url):
    data = get_raw_airline_fleet_data(url)
    result = process_raw_airline_fleet_data(data)
    return result

# Handle getting the all the flights

def get_raw_airline_flight_data(url):
    return get_raw_data(url, 'tbl-datatable', 'tbody','tr') or []


def process_raw_airline_flight_data(data):
    result = []
    for entry in data:
        cells = entry.find_all('td')
        if cells:
            record = {}
            record['flight'] = encode_and_get(cells[1].text)
            record['from'] = cells[2]['title']
            record['to'] = cells[3]['title']
            record['aircraft-type'] = encode_and_get(cells[4].text)
            link = cells[5].find('a')
            if link:
                record['aircraft'] = encode_and_get(link.text)
            result.append(record)
    return result


def get_airline_flight_data(url):
    data = get_raw_airline_flight_data(url)
    result = process_raw_airline_flight_data(data)
    return result
