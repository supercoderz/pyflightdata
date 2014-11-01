import requests
from bs4 import BeautifulSoup

def get_page_or_none(url):
	try:
		result = requests.get(url)
	except:
		return None
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
