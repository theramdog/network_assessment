__author__ = 'Zachary Hill'

import requests
from bs4 import BeautifulSoup
import pprint

########################################################################################################################
# Hard coded variables the End of Life website
# Cisco End of Life device listings url
eol_url = requests.get('http://www.cisco.com/c/en/us/products/eos-eol-listing.html')
html = BeautifulSoup(eol_url.text, 'html.parser')
parsed_soup = html.find_all('span', {'class': ['contentContent', 'contentLink']})
eol_list = []


# Splits out BeautifulSoup output elements into a list where each item is a single string or device.
for element in parsed_soup:
    eol_list.append(element.get_text())


pprint.pprint(eol_list)
