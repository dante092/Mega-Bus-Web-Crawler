import megabus
import time

print('MEGABUS CRAWLER')
url = megabus.params('New York, ny', 'Boston, MA', '4/20/2016', '4/20/2016')

time.sleep(3)
html = megabus.download_data(url)
megabus.params_message(html)
trip1 = megabus.download_trips(url)



for i in trip1:
    data = megabus.Trip(i)
    print(i)
    data.build_trip()


 # Need to get time and 

