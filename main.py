import megabus
import time

import re
import os
import sys
from urllib.request import urlopen
from bs4 import BeautifulSoup

print('MEGABUS CRAWLER')

#origin = input('From: ')
#destination = input('Destination: ')
#leaving = input('Date of Departure: ')
#arrival = input('Date of Arrival: ')
#url = megabus.params(origin, destination, leaving, arrival)

url = megabus.params('New York, ny', 'Boston, MA', '4/18/2016', '4/18/2016')
html = megabus.download_data(url)

megabus.params_message(html)
time.sleep(3)
trip1 = megabus.download_trips(url)

for i in trip1:
    print(i)


 # Need to get time and 
