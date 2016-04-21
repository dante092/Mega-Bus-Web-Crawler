import shelve
import time
import megabus
from collections import deque

print('MEGABUS CRAWLER'.center(70, '='))

url = megabus.format('New York, ny', 'Boston, MA', '4/20/2016', '4/20/2016')
#url = megabus.get_params()
time.sleep(3)
html = megabus.download_data(url)


# Displays a summary of the trip that is being searched
megabus.params_message(html)
id = 0 # numerical number used to display current trip.

while True:
    # Downloads HTML using URL, gets all availible trips.
    trip = megabus.download_trips(url, id)
    if trip == []: # An empty list means we reached the end of the road. 
        print('\nNo more trips for the day.')
        break
    # Selects the Trip based on ID provided before in download_trips, ID is
    # passed once more but only to be able to print the currebt ID number. 
    for data_row in trip:
        data = megabus.Trip(data_row, id)
        data.build_trip()
    id += 1

