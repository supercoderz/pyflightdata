# coding: utf-8
import requests
result = requests.get('http://www.flightradar24.com/data/flights/ac16/')
result.status_code
from bs4 import BeautifulSoup
soup = BeautifulSoup(result.content)
soup.find(id='tblFltData')
soup.find(id='tblFlightData')
soup.find(id='tblFlightData').tr
soup.find(id='tblFlightData').tr
soup.find(id='tblFlightData').find_all('tr')
soup.find(id='tblFlightData').find_all('tr').size()
soup.find(id='tblFlightData').find_all('tr').__len__()
soup.find(id='tblFlightData').find_all('tr')[4]
type(soup.find(id='tblFlightData').find_all('tr')[4])
dir(soup.find(id='tblFlightData').find_all('tr')[4])
type(soup.find(id='tblFlightData').find_all('tr')[4])
type(soup.find(id='tblFlightData').find_all('tr')[4])
e = soup.find(id='tblFlightData').find_all('tr')[4]
e
e.td
e.td
e.attrs
e.children
e
e.sttrs
e.attrs
e.decompose
e.decompose()
e
e = soup.find(id='tblFlightData').find_all('tr')[4]
e.attrs
e.find_all('td')
dir(e.find_all('td')[1])
(e.find_all('td')[1]).attrs
(e.find_all('td')[1]).text
(e.find_all('td')[1])
(e.find_all('td')
)
get_ipython().magic(u'save testing 1-38')
