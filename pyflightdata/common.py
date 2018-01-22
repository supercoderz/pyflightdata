import json
import sys

import requests
from bs4 import BeautifulSoup
from jsonpath_rw import parse
from requests import Session


class FlightMixin(object):

    session = Session()
    AUTH_TOKEN = ''


class ProcessorMixin(object):

    def json_loads_byteified(self, json_text):
        if type(json_text) == bytes:
            json_text = json_text.decode('utf-8')
        return self._byteify(
            json.loads(json_text, object_hook=self._byteify),
            ignore_dicts=False
        )

    def _byteify(self, data, ignore_dicts=False):
        # if this is a unicode string, return its string representation
        if isinstance(data, str):
            return self.encode_and_get(data)
        if sys.version_info[0] < 3 and isinstance(data, unicode):
            return self.encode_and_get(data)
        # if this is a list of values, return list of byteified values
        if isinstance(data, list):
            return [self._byteify(item, ignore_dicts=True) for item in data]
        # if this is a dictionary, return dictionary of byteified keys and values
        # but only if we haven't already byteified it
        if isinstance(data, dict) and not ignore_dicts:
            return {
                self._byteify(key, ignore_dicts=False): self._byteify(value, ignore_dicts=False)
                for key, value in data.items()
            }
        # if it's anything else, return it in its original form
        return data

    def put_to_page(self, url, params):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                'Method': 'POST',
                'Origin': 'https://www.flightradar24.com',
                'Referer': 'https://www.flightradar24.com'
            }
            result = FlightMixin.session.put(
                url, headers=headers, params=params)
        except:
            return None
        return self.json_loads_byteified(result.content) if result.status_code == 200 else None

    def get_page_or_none(self, url):
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0',
                'Origin': 'https://www.flightradar24.com',
                'Referer': 'https://www.flightradar24.com'
            }
            result = FlightMixin.session.get(url, headers=headers)
        except:
            return None
        return result.content if result.status_code == 200 else None

    def get_soup_or_none(self, content):
        try:
            return BeautifulSoup(content, "lxml", from_encoding='utf-8')
        except:
            return None

    def traverse(self, soup, key, elements, by_class=False):
        res = soup.find(id=key) if not by_class else soup.find(class_=key)
        if elements:
            for element in elements[:-1]:
                res = res.find(element)
            return res.find_all(elements[-1])
        return res

    def get_raw_data(self, url, elemid, *elements):
        content = self.get_page_or_none(url)
        if content:
            soup = self.get_soup_or_none(content)
            if soup:
                return self.traverse(soup, elemid, elements)

    def get_raw_data_class(self, url, klass, *elements):
        content = self.get_page_or_none(url)
        if content:
            soup = self.get_soup_or_none(content)
            if soup:
                return self.traverse(soup, klass, elements, True)

    def get_raw_data_class_all(self, url, klass):
        content = self.get_page_or_none(url)
        if content:
            soup = self.get_soup_or_none(content)
            if soup:
                return soup.find_all(class_=klass)

    def get_raw_data_json(self, url, path):
        content = self.get_page_or_none(url)
        if content:
            try:
                content_json = self.json_loads_byteified(content)
                expr = parse(path)
                return [match.value for match in expr.find(content_json)]
            except:
                pass

    def encode_and_get(self, string):
        if sys.version_info[0] < 3:
            return string.encode('unicode-escape').replace('\\xa0', ' ')
        else:
            return string.encode('unicode-escape').replace(b'\\xa0', b' ').decode('utf-8')
