""" Create a program that texts or emails me everytime if finds a cheap ticket in megabus.com
"""
import re
import os
import time
from urllib.request import urlopen
from  urllib.error import URLError
import urllib.request
from bs4 import BeautifulSoup
import random

from time import sleep
import sys

def progress_bar(speed=1.00):
    for i in range(21):
        sys.stdout.write('\r')
        # the exact output you're looking for:
        sys.stdout.write("[%-20s] %d%%" % ('='*i, 5*i))
        sys.stdout.flush()
        sleep(speed)



class Trip():
    """ Models a megabus trip."""

    def __init__(self, data, number, mode, crawling_day):
        """ Initializes basic trip Data."""
        self.data = data
        self.trip_number = number
        self.mode = mode
        self.day = crawling_day

    def price(self, verbose=True):
        """
        Returns the price of the trip, and prints the price if verbose is set to True
        :return: price = int
        """
        data = self.data
        price_regex = re.compile(r"\$\d\d")  # Dollard Sign followed by two digits.
        matches = price_regex.findall(data)
        price = matches[0]
        if verbose == True:
            print('Price: ', price)
        price = price.replace('$', '')  # Cleans up data, so it can be converted to int easier later.
        return int(price)  # only price gets returned, to get a list of prices, pass a list as a parameter.

    def departure_time(self):
        """Gets & Prints the departure time, :Returns: departure_time = str """
        data = self.data
        departure_regex = re.compile(r"^(Departs\d+:\d\d...)")  # DepartsDigitormore, :, two more digits
        matches = departure_regex.findall(data)
        departure_time = matches[0]
        departure_time = departure_time.replace('Departs', '')
        print('Departing: ', departure_time)
        return departure_time

    def arrival_time(self):
        """Gets & Prints the arrival time, :Returns: arrival_time = str """
        data = self.data
        arrival_regex = re.compile(r"(Arrives\d+:\d\d...)")
        matches = arrival_regex.findall(data)
        arrival_time = matches[0]
        arrival_time = arrival_time.replace('Arrives', '')
        print('Arriving: ', arrival_time)
        return arrival_time

    def random_id(self):
        """ Generates four random numbers"""
        randomID = ''

        for number in range(0, 7):
            randomnumber = str(random.randint(0, 9))
            randomID = randomID + randomnumber

        return randomID

    def trip_id(self):
        """ Creates an unique Identifier for  each trip"""
        price = str(self.price(verbose=False))
        random_id = self.random_id()
        trip_id = random_id + price
        print('Trip ID: ', trip_id)
        return trip_id

    def display_trip(self):
        """ Displays some of the current trip attributes. """
        print('\n')
        if self.mode == 'inbound':
            print(' Outbound Trip {0} '.center(50, '=').format(self.trip_number + 1))
        if self.mode == 'outbound':
            print(' Inbound Trip {0} '.center(50, '=').format(self.trip_number + 1))
        self.trip_id()
        self.price()
        self.departure_time()
        self.arrival_time()


def generate_city_code(citi):
    """
    A dictionary of city codes used by megabus to identify each city.
    :return: The proper city code, string.
    """
    citi = citi.strip() # Strips the city provided of any extra spaces
    citi = citi.upper()
    citi_codes = {
        'ALBANY, NY': '89',
        'AMHERST, MA': '90',
        'ANN ARBOR, MI': '91',
        'ATLANTIC CITY, NJ': '92',
        'BINGHAMTON, NY': '93',
        'BOSTON, MA': '94',
        'BUFFALO, NY': '95',
        'BURLINGTON, VT': '96',
        'CAMDEN': '97',
        'CHAMPAIGN, IL': '98',
        'CHARLOTTE, NC': '99',
        'CHICAGO, IL': '100',
        'CHRISTIANSBURG, VA': '101',
        'CINCINNATI, OH': '102',
        'CLEVELAND, OH': '103',
        'COLUMBIA, MO': '104',
        'COLUMBUS, OH': '105',
        'DES MOINES, IA': '106',
        'DETROIT, MI': '107',
        'ERIE, PA': '108',
        'FREDERICK, MD': '109',
        'HAMPTON, VA': '110',
        'HARRISBURG, PA': '111',
        'HARTFORD, CT': '112',
        'HOLYOKE, CT': '113',
        'HYANNIS, MA': '114',
        'INDIANAPOLIS, IN': '115',
        'IOWA CITY, IA': '116',
        'KANSAS CITY, MO': '117',
        'KNOXVILLE, TN': '118',
        'MADISON, WI': '119',
        'MEMPHIS, TN': '120',
        'MILWAUKEE, WI': '121',
        'NEW HAVEN, CT': '122',
        'NEW YORK, NY': '123',
        'NIAGARA FALLS, ON': '124',
        'NORMAL, IL': '125',
        'OMAHA, NE': '126',
        'PHILADELPHIA, PA': '127',
        'PITTSBURGH, PA': '128',
        'PORTLAND, ME': '129',
        'PROVIDENCE, RI': '130',
        'DURHAM, NC': '131',
        'RICHMOND, VA': '132',
        'RIDGEWOOD, NJ': '133',
        'ROCHESTER, NY': '134',
        'SECAUCUS, NJ': '135',
        'ST LOUIS, MO': '136',
        'STATE COLLEGE, PA': '137',
        'STORRS, CT': '138',
        'SYRACUSE, NY': '139',
        'TOLEDO, OH': '140',
    }
    return citi_codes[citi] # Returns the city code to be formatted into an URL.


def generate_date(date):
    """
    Formats the provided date, returns: String
    """
    date = date
    date = date.replace('/', '\n')
    date = date.split()
    month, day, year = date[0], date[1], date[2]
    date = month + '%2f' + day + '%2f' + year
    return date


def format(origin, destination, crawling_date, passengers='2'):
    """ Formats a Megabus URL with the destination information."""
    base = 'http://us.megabus.com/JourneyResults.aspx?'
    origincode = 'originCode=' + generate_city_code(origin)
    destinationcode = '&destinationCode=' + generate_city_code(destination)   # Crawling date is provided twice
    departuredate = '&outboundDepartureDate=' + generate_date(crawling_date) # This is done to get both outgoing
    coming_back = '&inboundDepartureDate=' + generate_date(crawling_date)   # and ingoing trips with the same URL
    passengers = '&passengerCount=' + passengers
    rest_of_url = '&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=1'
    url = base + origincode + destinationcode + departuredate + coming_back + passengers + rest_of_url
    return url


def download_data(url):
    """ Dowloads data from Megabus.com """
    headers = {}
    headers['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
    request = urllib.request.Request(url, headers=headers)
    while True:  # loop to avoid program stopping after an URLError.
        try:
            #time.sleep(3) # slows down the requests.
            connect = urlopen(request)
            break

        except URLError as e: # This will loop indefenetly if connection is not found.
            print('Something is wrong', e, ' Attemting to fix it.\n')
            continue
    soup = BeautifulSoup(connect, 'html.parser')
    return soup


def params_message(soup):
    """ prints a consise message of the search being done """
    soup = soup
    message = []
    # The message is stored under tag div, in class "search_params"
    print('|SEARCHING FOR TRIP TO|')
    for word in soup.findAll('div', {"class": "search_params"}):
        message.append(word.getText())

    for word in message:
        # Removes tabs and space.
        word = word.replace('\t', '')
        word = word.replace('\n', '')
        print(word)

def format_trip_id(number, mode):
    """formats the ID to be search with the numerical id(number)"""
    # This functions returns the link to be used to search for trips.
    # mode refers to whereever the trip is inbound or outbound.
    # This function is equipped to deal with both
    # incoming trips and outgoing trips.
    # ID is converted from int to str to be able to concantanate with url.
    if mode == 'inbound':
        if number > 9:
            # If ID is a two digit number, it formats the last two digits.
            number = str(number)
            id = 'JourneyResylts_InboundList_GridViewResults_ctl07_row_item'
            id = id.replace('07', number)
            return id
        else:
            # If Id is a one digit number, it formats the last digit only.
            number = str(number)
            id = 'JourneyResylts_InboundList_GridViewResults_ctl07_row_item'
            id = id.replace('7', number)
            return id # returns the formatted ID to be used to search for trips

    if mode == 'outbound':
        if number > 9:
            number = str(number)
            id = 'JourneyResylts_OutboundList_GridViewResults_ctl09_row_item'
            id = id.replace('09', number)
            return id
        else:
            number = str(number)
            id = 'JourneyResylts_OutboundList_GridViewResults_ctl09_row_item'
            id = id.replace('9', number)
            return id
    else:
        print("Something is wrong with Mode")


def download_trips(url, id, mode):
    """Returns a string with the trip information """
    identification = format_trip_id(id, mode)
    html = download_data(url)
    temp = []
    trip = []
    for trip_data in html.findAll('ul', id=identification):
        temp.append(trip_data.getText())
    for word in temp:
        word = word.replace('\t', '')
        word = word.replace('\n', '')
        word = word.replace('\r', '')
        trip.append(word)
    return trip



def start_trips(url, mode, crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices):
    """Sorts through each row of data """

    data_from_trips = load_trips_into_memory(url, mode, crawling_day)
    read_trips(data_from_trips, mode, crawling_day,m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
               su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices )

    #id = 0  # numerical number used to display current trip.
    #print("\nDownloading {0}'s".format(crawling_day), mode,'Data')
    #progress_bar(1.00)
    #while True:
        # Downloads HTML using URL, gets all availible trips.
      #  megabus_trip = download_trips(url, id, mode)

       # if megabus_trip == []:  # An empty list means we reached the end of the road.
        #    break

        # Selects the Trip based on ID provided before in download_trips, ID is
        # passed once more but only to be able to print the currebt trip number.
        #for data_row in megabus_trip:
         #   data = Trip(data_row, id, mode, crawling_day)
          #  price = data.price(verbose=False)
           # record_price_to_list(mode, crawling_day,price,m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
            #                     su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices )

        #id += 1

def load_trips_into_memory(url, mode, crawling_day):
    data_from_trips = []
    id = 0  # numerical number used to display current trip.
    print("\nDownloading {0}'s".format(crawling_day), mode,'Data')
    progress_bar(0.20)

    while True:
        # Downloads HTML using URL, gets all availible trips.
        megabus_trip = download_trips(url, id, mode)
        if megabus_trip == []:  # An empty list means we reached the end of the road.
            break
        data_from_trips.append(megabus_trip)
        id += 1
    return data_from_trips

def read_trips(data_from_trips, mode, crawling_day,m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
               su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices ):
    id = 0
    for data_row in data_from_trips:
        id +=1
        data = Trip(data_row, id, mode, crawling_day)
        price = data.price(verbose=False)
        data.display_trip()
        record_price_to_list(mode, crawling_day,price,m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                   su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices )



def record_price_to_list(mode,crawling_day, trip_price, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                         su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices):
    """Records the provided price to list."""
    # crawling_day is used to determined to which list of days the price has to be appendend too.
    # Mode is used to determined wherever this is a inbound or outbound trip.
    #
    day = crawling_day
    price = trip_price
    mode = mode
    if mode == 'outbound':
        if day == 'Monday':
            m_prices.append(price)

        if day == 'Tuesday':
            t_prices.append(price)

        if day == 'Wednesday':
            w_prices.append(price)

        if day == 'Thursday':
            th_prices.append(price)

        if day == 'Friday':
            f_prices.append(price)

        if day == 'Saturday':
            s_prices.append(price)

        if day == 'Sunday':
            su_prices.append(price)

    if mode == 'inbound':
        if day == 'Monday':
            im_prices.append(price)

        if day == 'Tuesday':
            it_prices.append(price)

        if day == 'Wednesday':
            iw_prices.append(price)

        if day == 'Thursday':
            ith_prices.append(price)

        if day == 'Friday':
            if_prices.append(price)

        if day == 'Saturday':
            is_prices.append(price)

        if day == 'Sunday':
            isu_prices.append(price)


def compare_trip_prices(url, mode, crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices):
    """Sorts through each row of data """
    id = 0  # numerical number used to display current trip.
    while True:
        # Downloads HTML using URL, gets all availible trips.
        megabus_trip = download_trips(url, id, mode)

        if megabus_trip == []:  # An empty list means we reached the end of the road.
            break

        # Selects the Trip based on ID provided before in download_trips, ID is
        # passed once more but only to be able to print the currebt trip number.
        for data_row in megabus_trip:
            data = Trip(data_row, id, mode, crawling_day)
            price = data.price(verbose=False)
            a_list = get_price_list(mode, crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                                    su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices)
            average = 0
            for price_in_day in a_list:
                average += price_in_day

            average = average/len(a_list)
            print('Trip Price ', price,'Average Price ', average)

            if price <= int(average):
                print('Recommended Trip')
                data.display_trip()
        id += 1

def get_price_list(mode, crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                   su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices):
    mode = mode
    day = crawling_day.upper()
    if mode == 'outbound':
        if day == 'MONDAY':
            return m_prices

        if day == 'THURSDAY':
            return th_prices

        if day == 'WEDNESDAY':
            return w_prices

        if day == 'TUESDAY':
            return t_prices

        if day == 'FRIDAY':
            return f_prices

        if day == 'SATURDAY':
            return s_prices

        if day == 'SUNDAY':
            return su_prices

    if mode == 'inbound':
        if day == 'MONDAY':
            return im_prices

        if day == 'THURSDAY':
            return ith_prices

        if day == 'WEDNESDAY':
            return iw_prices

        if day == 'TUESDAY':
            return it_prices

        if day == 'FRIDAY':
            return if_prices

        if day == 'SATURDAY':
            return is_prices

        if day == 'SUNDAY':
            return isu_prices