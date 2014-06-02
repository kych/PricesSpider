import urllib2
import re
import numpy as np
import matplotlib.pyplot as plt
# import plotly

# py = plotly.plotly('changkaiye', '4cpqp1rork')
# priceTable = [['4395', '5295', '6195', '7095'], ['3588', '4288', '4988', '5688'], ['3888', '4688', '5488', '6288'], ['499', '599', '699', '799']]
priceTable = []
countryCodeList = ['SE', 'CN', 'HK', 'US']


# Currency Exchange
def exchange_rate( source_currency, dest_currency, amount ):
    url_exchange = urllib2.urlopen("http://rate-exchange.appspot.com/currency?from={0}&to={1}&q={2}".format(source_currency, dest_currency, amount))
    result = url_exchange.read()
    # print result
    return result[result.find('"v"') + 5 : result.rfind('.')]


# Get URLs of iPad product webpage in different countries
def url_ipad(countryCode):
    return "http://store.apple.com/" + countryCode + "/buy-ipad/ipad-air"


# Get prices for iPad WiFi 16G, 32G, 64G and 128G
def find_price(countryCode):
    priceRow = []
    link = url_ipad(countryCode)
    content = urllib2.urlopen(link).read()
    content = content.replace("\n", " ")
    content = content.replace("\r", " ")
    content = content.replace("\t", " ")

    match = re.findall(r'<span itemprop="price">(.*?)</span>', content)

    # Find prices and convert to SEK
    for price in match[0:4]:
        price = ''.join(e for e in price if e.isalnum())
        price = {
            'se': lambda price: price[:-4],
            'cn': lambda price: exchange_rate( 'CNY', 'SEK', price[3:]),
            'hk': lambda price: exchange_rate( 'HKD', 'SEK', price[2:]),
            'us': lambda price: exchange_rate( 'USD', 'SEK', price[:-2]),
        }[countryCode](price)
        # print "exchanged: " + price
        priceRow.append(price)

    priceTable.append(priceRow)


# Draw price comparison bars by matplotlib
def plot(priceTable):
    priceTable = np.array(priceTable)
    priceTable = priceTable.astype(np.int)

    N = len( priceTable[:,0] )
    # x = np.arange(1, N+1)
    ind = np.arange(N)  # the x locations for the groups
    width = 0.2       # the width of the bars

    fig, ax = plt.subplots()

    rects1 = ax.bar(ind, priceTable[0,:], width, color='b')
    rects2 = ax.bar(ind+width, priceTable[1,:], width, color='r')
    rects3 = ax.bar(ind+width*2, priceTable[2,:], width, color='g')
    rects4 = ax.bar(ind+width*3, priceTable[3,:], width, color='y')

    # add some
    ax.set_ylabel('Price in SEK')
    ax.set_title('iPad Price in different countries')
    ax.set_xticks(ind+width)
    ax.set_xticklabels( ('16G', '32G', '64G', '128G') )
    ax.legend( (rects1[0], rects2[0], rects3[0], rects4[0]), (countryCode for countryCode in countryCodeList) )
    plt.show()


def main():
    for countryCode in ["se", "cn", "hk", "us"]:
        find_price(countryCode)

    # Print prices diffrences in table
    print priceTable

    plot(priceTable)

    # for x in priceTable[1]:
    #     print x
    #     print exchange_rate('USD', 'SEK', x)


if __name__ == "__main__":
    main()
