import requests
from bs4 import BeautifulSoup
import sys
import json
from jsonpath_rw import parse


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
        soup = BeautifulSoup(content,"lxml")
        return soup
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
            try:
                return traverse(soup,elemid,elements)
            except:
                pass

def get_raw_data_class(url, klass, *elements):
    content = get_page_or_none(url)
    if content:
        soup = get_soup_or_none(content)
        if soup:
            try:
                return traverse(soup,klass,elements,True)
            except:
                pass

def get_raw_data_json(url, path):
    content = get_page_or_none(url)
    if content:
        try:
            content_json = json.loads(content)
            expr = parse(path)
            return [match.value for match in expr.find(content_json)]
        except:
            pass


def encode_and_get(string):
    if sys.version < '3':
        return string.encode('unicode-escape').replace('\\xa0', ' ')
    else:
        return string.encode('unicode-escape').replace(b'\\xa0', b' ')
