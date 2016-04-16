""" Small Script to find codes for MEGABUS"""
from urllib.request import urlopen
from bs4 import BeautifulSoup
number = 89
while True:
    try:
        url = 'http://us.megabus.com/JourneyResults.aspx?originCode={0}&destinationCode=143&outboundDepartureDate=4%2f16%2f2016&inboundDepartureDate=4%2f16%2f2016&passengerCount=2&transportType=0&concessionCount=0&nusCount=0&outboundWheelchairSeated=0&outboundOtherDisabilityCount=0&inboundWheelchairSeated=0&inboundOtherDisabilityCount=0&outboundPcaCount=0&inboundPcaCount=0&promotionCode=&withReturn=1'.format(number)
        html = urlopen(url)
        soup = BeautifulSoup(html)
        places = []
        for place in soup.findAll("strong"):
            places.append(place.getText())
        print("'"+places[0].upper()+"'"+' : '+"'"+str(number)+"'"+',')
        number += 1

    except IndexError:
        number +=1
        continue
    else:
        if number > 145:
            print('Done')
            break
