""" Small Script to find citi destinations codes for MEGABUS"""

from urllib.request import urlopen
from bs4 import BeautifulSoup

number = 89 # First city. 
while True:
    try:
        url = 'http://us.megabus.com/JourneyResults.aspx?originCode={0}&destinationCode=143&outboundDepartureDate=4%2f16%2f2016&inboundDepartureDate=4%2f16%2f2016&passengerCount=2&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=1'.format(number)
        html = urlopen(url)
        soup = BeautifulSoup(html)
        places = []
        for place in soup.findAll("strong"):# City name is in between a strong tag
            places.append(place.getText())
        print("'"+places[0].upper()+"'"+' : '+"'"+str(number)+"'"+',') # formats the city into a dictionary to be used later.
        number += 1

    except IndexError: #Some cities skip a digit or two, this code stops the indexerror from stopping the program.
        number +=1
        continue
    else:
        if number > 145: # This is the numerical code for the last city. 
            print('Done')
            break
"""" 
Sample Output : 

""""
