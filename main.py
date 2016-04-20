import shelve
import time
import megabus
morning = shelve.open('morning_prices')
afternoon = shelve.open('Afternoon_prices')

print('MEGABUS CRAWLER'.center(70, '='))
url = megabus.format('New York, ny', 'Boston, MA', '4/20/2016', '4/20/2016')

#url = megabus.get_params()
time.sleep(3)
html = megabus.download_data(url)

print('|SEARCHING FOR TRIP TO|')
megabus.params_message(html)

id = 0
while True:
    trip = megabus.download_trips(url, id)
    if trip == []:
        print('No more trips for the day.')
        break
    megabus.format_trip('5')
    for row in trip:
        data = megabus.Trip(row, id)
        data.build_trip()
    id += 1


 # Need to get time and 

