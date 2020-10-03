# MIT License
#
# Copyright (c) 2019 Hari Allamraju
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from .common import ProcessorMixin
from .json_helper import fltr

ROOT = 'http://www.flightradar24.com'
REG_BASE = 'https://api.flightradar24.com/common/v1/flight/list.json?query={0}&fetchBy=reg&page={2}&limit={3}&token={1}&timestamp={4}'
FLT_BASE = 'https://api.flightradar24.com/common/v1/flight/list.json?query={0}&fetchBy=flight&page={2}&limit={3}&token={1}'
AIRPORT_BASE = 'http://www.flightradar24.com/data/airports/{0}'
AIRPORT_DATA_BASE = 'https://api.flightradar24.com/common/v1/airport.json?code={0}&page={2}&limit={3}&token={1}'
AIRPORT_DATA_BASE_EARLIER = 'https://api.flightradar24.com/common/v1/airport.json?code={0}&plugin[]=&plugin-setting[schedule][mode]={5}&plugin-setting[schedule][timestamp]={4}&page={2}&limit={3}&token={1}'
AIRLINE_BASE = 'https://www.flightradar24.com/data/airlines/{0}'
AIRLINE_FLEET_BASE = 'https://www.flightradar24.com/data/airlines/{0}/fleet'
AIRLINE_FLT_BASE = 'https://www.flightradar24.com/v1/search/web/find?query={0}&limit={1}&type=schedule'
AIRLINE_FLT_BASE_POINTS = 'https://api.flightradar24.com/common/v1/search-mobile-pro.json?query=default&origin={0}&destination={1}'
IMAGE_BASE = 'https://www.flightradar24.com/aircrafts/images/?aircraft={0}'
LOGIN_URL = 'https://www.flightradar24.com/user/login'


class FR24(ProcessorMixin):

    FILTER_JSON_KEYS = ['hex', 'id', 'logo', 'row', 'icon']

    timestamp = ""

    # airport stats

    def filter_and_get_data(self, data):
        if data:
            res = data[0] or []
            return fltr(res, self.FILTER_JSON_KEYS)
        return []

    def get_airport_weather(self, url):
        data = self.get_raw_data_json(
            url, 'result.response.airport.pluginData.weather')
        return self.filter_and_get_data(data) or []

    def get_airport_stats(self, url):
        data = self.get_raw_data_json(
            url, 'result.response.airport.pluginData.details.stats')
        return self.filter_and_get_data(data) or []

    def get_airport_details(self, url):
        data = self.get_raw_data_json(
            url, 'result.response.airport.pluginData.details')
        return self.filter_and_get_data(data) or []

    def get_airport_reviews(self, url):
        data = self.get_raw_data_json(
            url, 'result.response.airport.pluginData.flightdiary')
        return self.filter_and_get_data(data) or []

    def get_airport_arrivals(self, url):
        data = self.get_raw_data_json(
            url, 'result.response.airport.pluginData.schedule.arrivals.data')
        return self.filter_and_get_data(data) or []

    def get_airport_departures(self, url):
        data = self.get_raw_data_json(
            url, 'result.response.airport.pluginData.schedule.departures.data')
        return self.filter_and_get_data(data) or []

    def get_airport_onground(self, url):
        data = self.get_raw_data_json(
            url, 'result.response.airport.pluginData.schedule.ground.data')
        return self.filter_and_get_data(data) or []

    def get_airport_metars_hist(self, url):
        data = self.get_raw_metars_hist(url)
        data = self.process_raw_metars_hist(data)
        return data

    def get_raw_metars_hist(self, url):
        return self.get_raw_data_class_all(url, 'master expandable')

    def process_raw_metars_hist(self, data):
        result = {}
        for d in data:
            cells = d.find_all('td')
            if cells:
                time = self.encode_and_get(cells[1].text.strip())
                metar = self.encode_and_get(cells[0].text.strip())
                result[time] = metar
        return result

    # Handle all the flights data

    def get_raw_flight_data(self, url):
        data = self.get_raw_data_json(url, 'result.response.data')
        return self.filter_and_get_data(data) or []

    def process_raw_flight_data(self, data, by_tail=False):
        # TODO check later if we need to parse this data - for now return full set
        l = len(data)
        self.timestamp = ""
        if l > 0: self.timestamp = data[l-1]['time']['other']['updated']
        return data

    def get_data(self, url, by_tail=False):
        data = self.get_raw_flight_data(url)
        return self.process_raw_flight_data(data, by_tail)

    # Handle getting countries

    def get_raw_country_data(self):
        return self.get_raw_data(AIRPORT_BASE.format(''), 'tbl-datatable', 'tbody', 'tr') or []

    def process_raw_country_data(self, data):
        result = []
        for entry in data:
            cells = entry.find_all('td')
            if cells:
                # this will break one day
                for cell in cells[1:2]:
                    link = cell.find('a')
                    if link and 'data-country' in link.attrs:
                        record = {}
                        self.process_country_link(link, record)
                        images = link.find_all('img')
                        self.process_country_image(images, record)
                        result.append(record)
        return result

    def process_country_image(self, images, record):
        if images:
            for image in images:
                record['img'] = image['data-bn-lazy-src']

    def process_country_link(self, link, record):
        for attr in link.attrs:
            if attr not in ['href', 'class', 'onclick', 'title']:
                attr_new = attr.replace('data-', '')
                record[attr_new] = link[attr]

    def get_countries_data(self):
        data = self.get_raw_country_data()
        return self.process_raw_country_data(data)

    # Handle getting the airports in a country
    def get_raw_airport_data(self, url):
        return self.get_raw_data(url, 'tbl-datatable', 'tbody', 'tr') or []

    def process_raw_airport_data(self, data):
        result = []
        for entry in data:
            cells = entry.find_all('td')
            if cells:
                for cell in cells:
                    link = cell.find('a')
                    if link and 'data-iata' in link.attrs:
                        record = {}
                        self.process_airports_link(link, record)
                        result.append(record)
        return result

    def process_airports_link(self, link, record):
        for attr in link.attrs:
            if attr not in ['href', 'class', 'onclick']:
                attr_new = attr.replace('data-', '')
                if attr_new == 'title':
                    attr_new = 'name'
                record[attr_new] = link[attr]

    def get_airports_data(self, url):
        data = self.get_raw_airport_data(url)
        return self.process_raw_airport_data(data)

    # handle aircraft information
    def get_aircraft_data(self, url):
        data = self.get_raw_data_json(url, 'result.response.aircraftInfo')
        return self.filter_and_get_data(data) or []

    def get_aircraft_image_data(self, url):
        data = self.get_raw_data_json(url, 'result.response.aircraftImages')
        return self.filter_and_get_data(data) or []

    # Handle getting all the airlines

    def get_raw_airlines_data(self, url):
        return self.get_raw_data(url, 'tbl-datatable', 'tbody', 'tr') or []

    def process_raw_airlines_data(self, data):
        result = []
        for entry in data:
            record = {}
            cells = entry.find_all('td')
            if cells:
                for cell in cells:
                    link = cell.find('a')
                    self.process_country_airlines(link, record)
                    self.process_callsign_fleet_size(cell, record)
            if len(record) > 0:
                result.append(record)
        return result

    def process_callsign_fleet_size(self, cell, record):
        if 'class' in cell.attrs and 'text-right' in cell['class']:
            value = self.encode_and_get(cell.text.strip())
            if 'aircraft' in value:
                record['fleet-size'] = value
            else:
                record['callsign'] = value

    def process_country_airlines(self, link, record):
        if link and 'data-country' in link.attrs:
            for attr in link.attrs:
                if attr not in ['href', 'class', 'onclick', 'target', 'data-country']:
                    attr_new = attr.replace('data-', '')
                    record[attr_new] = link[attr]
            href = link['href']
            if href:
                code = href.split('/')[-1:]
                record['airline-code'] = code[0]
            span = link.find('span')
            if span:
                images = span.find_all('img')
                self.process_country_image(images, record)

    def get_airlines_data(self, url):
        data = self.get_raw_airlines_data(url)
        return self.process_raw_airlines_data(data)

    # Handle getting the fleet

    def get_raw_airline_fleet_data(self, url):
        tables = self.get_raw_data_class_all(
            url, 'table table-condensed table-hover')
        rows = []
        for table in tables:
            rows.extend(table.find('tbody').find_all('tr'))
        return rows

    def process_raw_airline_fleet_data(self, data, authenticated):
        result = []
        for parent in data:
            record = {}
            cells = parent.find_all('td')
            record['reg'] = cells[0].find('a').text.strip()
            record['type'] = cells[1].text.strip()
            record['msn'] = 'requires user login'
            record['age'] = 'requires user login'
            if authenticated:
                record['msn'] = cells[2].text.strip()
                record['age'] = cells[3].text.strip()
            result.append(record)
        return result

    def get_airline_fleet_data(self, url, authenticated):
        data = self.get_raw_airline_fleet_data(url)
        return self.process_raw_airline_fleet_data(data, authenticated)

    # Handle getting the all the flights

    def get_airline_flight_data(self, url, by_airports=False):
        json_key = 'result.response.flight.data' if by_airports else 'results'
        data = self.get_raw_data_json(
            url, json_key)
        return self.filter_and_get_data(data) or []
