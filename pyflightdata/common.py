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
    if result.status_code == 200:
        return result.content
    else:
        print result.status_code
        return None


def get_soup_or_none(content):
    try:
        soup = BeautifulSoup(content,"lxml")
        return soup
    except:
        return None


def traverse(soup,item,elements):
    res = soup.find(id=item)
    if elements:
        for element in elements[:-1]:
            res = res.find(element)
        return res.find_all(elements[-1])
    return res

def get_raw_data(url, item, *elements):
    content = get_page_or_none(url)
    if content:
        soup = get_soup_or_none(content)
        if soup:
            try:
                return traverse(soup,item,elements)
            except:
                return []
        else:
            return []
    else:
        return []

def get_raw_data_json(url, path):
    content = get_page_or_none(url)
    if content:
        try:
            content_json = json.loads(content)
            expr = parse(path)
            res = [match.value for match in expr.find(content_json)]
            return res
        except:
            return []
    else:
        return []


def encode_and_get(string):
    if sys.version < '3':
        return string.encode('unicode-escape').replace('\\xa0', ' ')
    else:
        return string.encode('unicode-escape').replace(b'\\xa0', b' ')
