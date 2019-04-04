from urllib.request import urlopen as req
from bs4 import BeautifulSoup
from datetime import datetime
import time
from re import sub
from decimal import Decimal
from threading import Timer
import smtplib

"""x = datetime.today()
y = x.replace(day=x.day + 0, hour=18, minute=7, second=0, microsecond=0)
delta_t = y - x
secs = delta_t.seconds + 1"""


class Crypto:

    def __init__(self, crypto_name):
        self.crypto_name = crypto_name
        self.crypto_price = []

    def add_price(self, c_price):
        self.crypto_price.append(c_price)


name_Array = []
cryptoList = []


# this function will populate each crypto object in the list with its initial values of name and price
def crypto_scrape():
    price_array = []
    print("running first function")
    raw_url = 'https://coinmarketcap.com/'
    page = req(raw_url)
    page_html = page.read()
    page.close()
    page_soup = BeautifulSoup(page_html, "html.parser")
    table = page_soup.find(id="currencies")
    table2 = table.tbody
    crypto_containers = table2.find_all('tr')

    for container in crypto_containers:
        # names = container.find_all("td", {"class": "no-wrap currency-name"})
        cryptoNames = container.findAll("a", {"class": "currency-name-container link-secondary night-mode-bold"})
        name = cryptoNames[0].string
        name_Array.append(name)

    for container in crypto_containers:
        cryptoPrices = container.findAll("a", {"class": "price"})
        price = cryptoPrices[0].string
        price_array.append(price)

    print("Printing all Cryptocurrency name and prices:")

    for i in range(len(price_array)):
        print(name_Array[i], "  ", price_array[i])

    for i in range(len(price_array)):
        cryptoList.append(Crypto(name_Array[i]))
        cryptoList[i].add_price(price_array[0])
    print("Finished first scrape!")


# this function will continue to add updated price data to list of objects in order to track price changes

def crypto_scrape_continue():
    price_array = []
    raw_url = 'https://coinmarketcap.com/'
    page = req(raw_url)
    page_html = page.read()
    page.close()
    page_soup = BeautifulSoup(page_html, "html.parser")
    table = page_soup.find(id="currencies")
    table2 = table.tbody
    crypto_containers = table2.find_all('tr')
    counter = 1

    for container in crypto_containers:
        # names = container.find_all("td", {"class": "no-wrap currency-name"})
        cryptoNames = container.findAll("a", {"class": "currency-name-container link-secondary night-mode-bold"})
        name = cryptoNames[0].string
        name_Array.append(name)

    for container in crypto_containers:
        cryptoPrices = container.findAll("a", {"class": "price"})
        price = cryptoPrices[0].string
        price_array.append(price)

    print("Printing all Cryptocurrency name and prices:")

    for x in range(len(price_array)):
        print(name_Array[x], "  ", price_array[x])

    for y in range(len(price_array)):
        cryptoList[y].add_price(price_array[y])


crypto_scrape()
num_cycles = 3  # number of iterations
wait_time = 1 * 5  # in seconds

start = datetime.now()  # getting initial time

for i in range(num_cycles - 1):
    time.sleep(20)
    crypto_scrape_continue()
    """while (datetime.now() - start).total_seconds() < wait_time:
        time.sleep(1)  # time buffer between each check
        crypto_scrape_continue() #calling function
        start = datetime.now()"""

"""t = Timer(secs, crypto_scrape_continue())
t.start()"""

message = " "
#This function takes the price data and calculates the greatest net change between scraping intervals
def get_greatest_change():

    biggest_name = "n/a"
    biggest_price = 0
    biggest_change = 0
    #loop through all 100
    for x in range (len(cryptoList)):
        first = cryptoList[x].crypto_price[0]
        firstval = Decimal(sub(r'[^\d.]', '', first))
        num_intervals = len(cryptoList[0].crypto_price)
        last = cryptoList[x].crypto_price[num_intervals - 1]
        lastval = Decimal(sub(r'[^\d.]', '', last))
        difference = lastval / firstval
       # print(difference)
        if((difference > biggest_change) and (difference != 1)):
            biggest_change = difference
            biggest_name = cryptoList[x].crypto_name
            biggest_price = last

    percent = biggest_change*100
   # print("%s has the greatest increase in price by %f percent since day 1" % (biggest_name, percent))
    message = ("%s has the greatest increase in price by %.2f percent since day 1" % (biggest_name, percent))
    print(message)

get_greatest_change()



def email_alert():
    content = message
    mail = smtplib.SMTP('smtp.gmail.com', 587)
    mail.ehlo()
    mail.starttls()
    mail.login('fjordsailer10@gmail.com', 'zzaaqq11')
    print(content)
    mail.sendmail('fjordsailer10@gmail.com', 'pmk765@gmail.com', content)
    mail.close()

email_alert()