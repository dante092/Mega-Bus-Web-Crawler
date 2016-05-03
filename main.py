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

#def run_spider():
print(r"""

_____________________________________
!\/        !        \/         ./
!/\        !        |\       ./
!  \       !       /  \    ./
!   \______!______|    \ ,/
!   /\     !    ./\    ,/
! /   \    !    |  \ ,/
!/     \___!____|  ,/
!     / \ _!__ *\,/
!    !   \ !  \,/
!    !  | \! ,/
!----------K/
!    ! ,!  /|
!    !/   / |
!   / \  /  |
!\./   \/   |
!/\    /    |
!  \  /    .o.
!   \/     :O:    MEGABUS CRAWLER
!   /       "
!  /
! /
!/
!
!
!""")
input('$ Press Enter to release Spider...')
print(r"""
          |
          |
      /   |   \
     / /  |  \ \
     \ \_(*)_/ /
      \_(~:~)_/
       /-(:)-\
      / / * \ \
      \ \   / /
       \     /
""")
print('$ Initializing Price Analysis: ')
megabus.progress_bar(0.20)
print('\n')

#origin = input('From: ')
#destination = input('Destination: ')

crawling = megabus_date.Date()
crawling_date = crawling.format_date()
crawling_day = crawling.day_of_the_week()





url = megabus.format('New York, ny', 'Boston, MA', crawling_date)

# Displays a summary of the trip that is being searched
#2megabus.params_message(html)

daysSpan = 5
# collect data
for number in range(0,daysSpan):
    if crawling_date == -1:
        break

    outbound = megabus.start_trips(url, 'outbound', crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                               su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices)

    inbound =  megabus.start_trips(url,'inbound', crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                               su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices)

    crawling.increment_day()
    crawling_day = crawling.day_of_the_week()

# compare data
crawling = megabus_date.Date()
crawling_day = crawling.day_of_the_week()


for number in range(0,daysSpan):
    megabus.compare_trip_prices(url, 'outbound', crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                                   su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices)

    megabus.compare_trip_prices(url,'inbound', crawling_day, m_prices, t_prices,w_prices,th_prices,f_prices,s_prices,
                                   su_prices, im_prices, it_prices,iw_prices,ith_prices,if_prices,is_prices,isu_prices)

    crawling.increment_day()
    crawling_day = crawling.day_of_the_week()



