import megabus
import megabus_date


# outbound prices
m_prices = []
t_prices = []
w_prices = []
th_prices = []
f_prices = []
s_prices = []
su_prices = []

# inbound price list
im_prices = []
it_prices = []
iw_prices = []
ith_prices = []
if_prices = []
is_prices = []
isu_prices = []
# Todo: Use Json to store city codes.

print('MEGABUS CRAWLER'.center(70, '='))

#origin = input('From: ')
#destination = input('Destination: ')

print('\nENTER Start Crawling Date')

year = int(input('Year: '))
month = int(input('Month: '))
day = int(input('Day:'))

crawling = megabus_date.Date(year, month, day)
crawling_date = crawling.format_date()
crawling_day = crawling.day_of_the_week()

url = megabus.format('New York, ny', 'Boston, MA', crawling_date)


# Displays a summary of the trip that is being searched
#2megabus.params_message(html)

# collect data
for number in range(0, 1):
    if crawling_date == -1:
        break

    outbound = megabus.start_trips(url, 'outbound', crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                               su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices)

    inbound =  megabus.start_trips(url,'inbound', crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                               su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices)
    trip_day = day + 1
    crawling = megabus_date.Date(year, month, trip_day)
    crawling_date = crawling.format_date()
    crawling_day = crawling.day_of_the_week()

# compare data
crawling = megabus_date.Date(year, month, day)
crawling_date = crawling.format_date()
crawling_day = crawling.day_of_the_week()


for number in range(0, 1):
    megabus.compare_trip_prices(url, 'outbound', crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                                   su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices)

    megabus.compare_trip_prices(url,'inbound', crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                                   su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices)
    day = day + 1
    crawling = megabus_date.Date(year, month, day)
    crawling_date = crawling.format_date()
    crawling_day = crawling.day_of_the_week()




