""" Create a program that texts or emails me everytime if finds a cheap ticket in megabus.com
"""
import re
import shelve
from urllib.request import urlopen
from  urllib.error import URLError
import urllib.request 
from bs4 import BeautifulSoup

#Todo: Use Json to store city codes.

class Trip():
    """ Models a megabus trip.
    """
    def __init__(self, data, number, prices=[]):
        self.data = data
        self.trip_number = number
        self.prices = prices


    def price(self):
        """
        Gets the price of the current trip
        :return: price = int
        """
        prices = self.prices
        data = self.data
        price_regex = re.compile(r"\$\d\d")
        matches = price_regex.findall(data)
        price = matches[0]
        print('Price: ', price)
        price = price.replace('$', '')
        prices.append(int(price))
        return price

    def departure_time(self):
        data = self.data
        departure_regex = re.compile(r"^(Departs\d+:\d\d...)")
        matches = departure_regex.findall(data)
        departure_time = matches[0]
        departure_time = departure_time.replace('Departs', '')
        print('Departing: ', departure_time)
        return departure_time

    def arrival_time(self):
        data = self.data
        arrival_regex = re.compile(r"(Arrives\d+:\d\d...)")
        matches = arrival_regex.findall(data)
        arrival_time = matches[0]
        arrival_time = arrival_time.replace('Arrives','')
        print('Arriving: ', arrival_time)
        return arrival_time

    def build_trip(self):
        print('\n')
        print(' Trip {0} '.center(50, '=').format(self.trip_number))
        self.price()
        self.departure_time()
        self.arrival_time()

def generate_city_code(citi):
    """
    :return: The proper city code, string.
    """
    citi = citi.strip()
    citi = citi.upper()
    citi_codes = {
            'ALBANY, NY' : '89',
            'AMHERST, MA' : '90',
            'ANN ARBOR, MI' : '91',
            'ATLANTIC CITY, NJ' : '92',
            'BINGHAMTON, NY' : '93',
            'BOSTON, MA' : '94',
            'BUFFALO, NY' : '95',
            'BURLINGTON, VT' : '96',
            'CAMDEN' : '97',
            'CHAMPAIGN, IL' : '98',
            'CHARLOTTE, NC' : '99',
            'CHICAGO, IL' : '100',
            'CHRISTIANSBURG, VA' : '101',
            'CINCINNATI, OH' : '102',
            'CLEVELAND, OH' : '103',
            'COLUMBIA, MO' : '104',
            'COLUMBUS, OH' : '105',
            'DES MOINES, IA' : '106',
            'DETROIT, MI' : '107',
            'ERIE, PA' : '108',
            'FREDERICK, MD' : '109',
            'HAMPTON, VA' : '110',
            'HARRISBURG, PA' : '111',
            'HARTFORD, CT' : '112',
            'HOLYOKE, CT' : '113',
            'HYANNIS, MA' : '114',
            'INDIANAPOLIS, IN' : '115',
            'IOWA CITY, IA' : '116',
            'KANSAS CITY, MO' : '117',
            'KNOXVILLE, TN' : '118',
            'MADISON, WI' : '119',
            'MEMPHIS, TN' : '120',
            'MILWAUKEE, WI' : '121',
            'NEW HAVEN, CT' : '122',
            'NEW YORK, NY' : '123',
            'NIAGARA FALLS, ON' : '124',
            'NORMAL, IL' : '125',
            'OMAHA, NE' : '126',
            'PHILADELPHIA, PA' : '127',
            'PITTSBURGH, PA' : '128',
            'PORTLAND, ME' : '129',
            'PROVIDENCE, RI' : '130',
            'DURHAM, NC' : '131',
            'RICHMOND, VA' : '132',
            'RIDGEWOOD, NJ' : '133',
            'ROCHESTER, NY' : '134',
            'SECAUCUS, NJ' : '135',
            'ST LOUIS, MO' : '136',
            'STATE COLLEGE, PA' : '137',
            'STORRS, CT' : '138',
            'SYRACUSE, NY' : '139',
            'TOLEDO, OH' : '140',
        }
    return citi_codes[citi]

def generate_date(date):
    """
    Formats the provided date, returns: String
    """
    date = date
    date = date.replace('/', '\n')
    date = date.split()
    month, day, year = date[0],date[1],date[2]
    date = month + '%2f' + day + '%2f' + year
    return date

def get_params():
    origin = input('From: ')
    destination = input('Destination: ')
    leaving = input('Date of Departure: ')
    arrival = input('Date of Arrival: ')
    url = format(origin, destination, leaving, arrival)
    return url

def format(origin, destination, leaving, comingback, passengers = '2' ):
    """ Formats a Megabus URL with the destination information."""
    base = 'http://us.megabus.com/JourneyResults.aspx?'
    origincode = 'originCode=' + generate_city_code(origin)
    destinationcode = '&destinationCode=' + generate_city_code(destination)
    departuredate = '&outboundDepartureDate=' + generate_date(leaving)
    coming_back ='&inboundDepartureDate=' + generate_date(comingback)
    passengers = '&passengerCount='+passengers
    rest_of_url = '&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=1'
    url = base + origincode + destinationcode + departuredate +coming_back + passengers + rest_of_url
    return url

def download_data(url):
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    request  = urllib.request.Request(url, headers=headers)
    while True:
        try:
            connect = urlopen(request)
            break
        except URLError as e:
            print('Something is wrong', e)
            continue

    soup = BeautifulSoup(connect, 'html.parser')
    return soup

def params_message(soup):
    soup = soup
    message = []
    
    for word in soup.findAll('div', {"class":"search_params"}):
        message.append(word.getText())
	
    for word in message:
        word = word.replace('\t','')
        word = word.replace('\n', '')
        print(word)

def format_trip(number):
    number = str(number)
    id ='JourneyResylts_OutboundList_GridViewResults_ctl09_row_item'
    id = id.replace('9', number)
    return id

def download_trips(url, id):
    identification = format_trip(id)
    html = download_data(url)
    temp = []
    trip = [] 
    for trip_data in html.findAll('ul', id = identification):
        temp.append(trip_data.getText())
    for word in temp:
        word = word.replace('\t','')
        word = word.replace('\n', '')
        word = word.replace('\r', '')
        trip.append(word)
        
    return trip
    
    



#todo: Sort out prices,and trip times
#todo: Compare prices to a set defenition of cheap
#todo: Record prices into a database for future comparison.
#todo: the price is rigth, shoot me a text with the info
#todo: the price is rigth, shoot me a text with the info

