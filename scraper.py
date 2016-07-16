from bs4 import *
from urllib import urlopen
from monitorList import *
import time

def checkStock(websiteName, url, soup):
    # inStock = False

    getPriceData(websiteName, soup)

    inStock = getStockData(websiteName, soup)
    return inStock


def getStockData(websiteName, soup):

    if websiteName == "ebay":
        # If the alert is found, it's out of stock
        if len(soup.find_all('div', {'class': 'msg yellow'})) != 0:
            return False

    elif websiteName == "newegg":
        itemJsonData = getNeweggData(soup)

        for item in itemJsonData.split(","):
            if "product_instock" in item:
                # If there's a 0, that means it's out of stock
                if "0" in item.split(":")[1][2]:
                    return False
                break

    elif websiteName == "acerrecertified":
        # If the alert is present, that means it's out of stock
        if len(soup.find_all('div', {'class': 'alert alert-danger'})) != 0:
            return False

    elif websiteName == "benqdirect":
        # If the out-of-stock class is found, return that it's out of stock
        if len(soup.find_all('p', {'class': 'availability out-of-stock'})) != 0:
            return False

    return True


def getPriceData(websiteName, soup):
    if websiteName == "ebay":
        for item in soup.find_all('span', {'itemprop': 'price'}):
            return item.attrs['content']

    elif websiteName == "newegg":
        # <meta content="399.99" itemprop="price"/>
        for item in soup.find_all('meta', {'itemprop': 'price'}):
            return item['content']

    elif websiteName == "benqdirect":
        # Yikes this got ugly, but I don't care for this price because the Ebay one is cheaper
        # for item in soup.find_all('p', {'class': 'special-price'}):
        #     print item
        price = soup('p', {'class': 'special-price'})
        return price[0]('span')[1].text.replace("$", " ").strip()

    elif websiteName == "acerrecertified":
        # I don't really care for the price of these. Just want to know when they're in stock
        for item in soup.find_all('span', {'id': 'unitprice'}):
            return item.text.replace("$", "")


def getNeweggData(soup):
        lineIndex = 0
        startIndex = 0
        soupSplit = soup.text.splitlines()
        itemJsonData = "{"

        while lineIndex < len(soupSplit):
            currentLine = soupSplit[lineIndex]

            # If the beginning of utag_data has been found, append the following lines and break once end of var
            if startIndex != 0:
                itemJsonData += currentLine.lstrip()
                if "}" in currentLine:
                    break
            elif "var utag_data = {" in currentLine:
                startIndex = lineIndex

            lineIndex += 1

        return itemJsonData


def main():
    print "----" * 3 + "\nBenq XL2730Z\n" + "----" * 3
    for url in monBenq:
        website = url.split(".")[1]
        monitorPage = urlopen(url)
        soup = BeautifulSoup(monitorPage, "html.parser")
        if checkStock(website, url, soup):
            print "Website : {0}\n" \
                  "Price   : {1}\n" \
                  "URL     : {2}\n".format(website, getPriceData(website, soup), url)

    print "----" * 3 + "\nAcer XG270HU\n" + "----" * 3
    for url in monAcer:
        website = url.split(".")[1]
        monitorPage = urlopen(url)
        soup = BeautifulSoup(monitorPage, "html.parser")
        if checkStock(website, url, soup):
            print "Website : {0}\n" \
                  "Price   : {1}\n" \
                  "URL     : {2}\n".format(website, getPriceData(website, soup), url)

    print "----" * 3 + "\nAsus MG278Q\n" + "----" * 3
    for url in monAsus:
        website = url.split(".")[1]
        monitorPage = urlopen(url)
        soup = BeautifulSoup(monitorPage, "html.parser")
        if checkStock(website, url, soup):
            print "Website : {0}\n" \
                  "Price   : {1}\n" \
                  "URL     : {2}\n".format(website, getPriceData(website, soup), url)
        # print "{0} : {1}".format(checkStock(website, url, soup), website)

while True:
    main()
    print "\nSleeping for 5 minutes"
    time.sleep(300)
    print "=-=-=-=-=-=-" * 3

#     if websiteName == "newegg":
#         monitorID = url.split("Item=")[1]
#         monitorJsonData = json.load(urlopen("http://apis.rtainc.co/newegg/item/" + monitorID))
#         if str(monitorJsonData[u'in_stock']) == "False":
#             return True
#     return False
# def getDataFromURL(websiteName, url):
#
#        for item in soup.find_all('script', {'type': 'text/javascript'}):
#             if "var utag_data" in str(item):
#                 print item