import requests
from bs4 import BeautifulSoup
import sys
import json
from jsonpath_rw import parse

def json_load_byteified(file_handle):
    return _byteify(
        json.load(file_handle, object_hook=_byteify),
        ignore_dicts=True
    )

def json_loads_byteified(json_text):
    return _byteify(
        json.loads(json_text, object_hook=_byteify),
        ignore_dicts=True
    )

def _byteify(data, ignore_dicts = False):
    # if this is a unicode string, return its string representation
    if isinstance(data, unicode):
        return encode_and_get(data)
    # if this is a list of values, return list of byteified values
    if isinstance(data, list):
        return [ _byteify(item, ignore_dicts=True) for item in data ]
    # if this is a dictionary, return dictionary of byteified keys and values
    # but only if we haven't already byteified it
    if isinstance(data, dict) and not ignore_dicts:
        return {
            _byteify(key, ignore_dicts=True): _byteify(value, ignore_dicts=True)
            for key, value in data.iteritems()
        }
    # if it's anything else, return it in its original form
    return data

def get_page_or_none(url):
    try:
        headers = {
            'User-Agent': 'pyflightdata'
        }
        result = requests.get(url,headers=headers)
    except:
        return None
    return result.content if result.status_code == 200 else None

def get_soup_or_none(content):
    try:
        return BeautifulSoup(content,"lxml")
    except:
        return None


def traverse(soup,key,elements,by_class=False):
    res = soup.find(id=key) if not by_class else soup.find(class_=key)
    if elements:
        for element in elements[:-1]:
            res = res.find(element)
        return res.find_all(elements[-1])
    return res

def get_raw_data(url, elemid, *elements):
    content = get_page_or_none(url)
    if content:
        soup = get_soup_or_none(content)
        if soup:
            return traverse(soup,elemid,elements)

def get_raw_data_class(url, klass, *elements):
    content = get_page_or_none(url)
    if content:
        soup = get_soup_or_none(content)
        if soup:
            return traverse(soup,klass,elements,True)

def get_raw_data_class_all(url, klass):
    content = get_page_or_none(url)
    if content:
        soup = get_soup_or_none(content)
        if soup:
            return soup.find_all(class_=klass)

def get_raw_data_json(url, path):
    content = get_page_or_none(url)
    if content:
        try:
            content_json = json_loads_byteified(content)
            expr = parse(path)
            return [match.value for match in expr.find(content_json)]
        except:
            pass


def encode_and_get(string):
    if sys.version < '3':
        return string.encode('unicode-escape').replace('\\xa0', ' ')
    else:
        return string.encode('unicode-escape').replace(b'\\xa0', b' ')
