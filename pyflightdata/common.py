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

import json
import sys
import time

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
            if result.status_code != 200:
                print("HTML code {0} - Retry in 10 seconds...".format(result.status_code))
                time.sleep(10)
                result = FlightMixin.session.get(url, headers=headers)
        except:
            return None
        return result.content if result.status_code == 200 else None

    def get_soup_or_none(self, content):
        try:
            return BeautifulSoup(content, "html5lib", from_encoding='utf-8')
        except:
            return None

    def traverse(self, soup, key, elements, by_class=False):
        results = []
        # Logic
        # Get the key element
        # Loop on each element except the last one
        # This is to traverse to the last element which is what we need
        # Once done with the list, if element is not none, get the needed value from there
        # Handle multiple results in each level
        res = soup.find_all(attrs={'id': key}) if not by_class else soup.find(
            attrs={'class': key})
        if elements:
            for element in elements[:-1]:
                next_level = []
                for r in res:
                    next_level.extend(r.find_all(element))
                res = next_level
            for r in res:
                results.extend(r.find_all(elements[-1]))
            return results
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
                return soup.find_all(attrs={'class': klass})

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
