from bs4 import *
from urllib import urlopen
from monitorList import *
import time


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


class Monitor:
    def __init__(self, url):
        self.url = url
        self.website = url.split(".")[1]
        self.soup = BeautifulSoup(urlopen(url), "html.parser")
        self.available = self.getStock()
        self.price = self.getPrice()
        self.name = self.getName()

    def getStock(self):
        if self.website == "ebay":
            # If the alert is found, it's out of stock
            if len(self.soup.find_all('div', {'class': 'msg yellow'})) != 0:
                return False
        elif self.website == "benqdirect":
            if len(self.soup.find_all('p', {'class': 'availability out-of-stock'})) != 0:
                return False
        elif self.website == "acerrecertified":
            if len(self.soup.find_all('div', {'class': 'alert alert-danger'})) != 0:
                return False
        return True

    def getPrice(self):
        if self.website == "ebay":
            for item in self.soup.find_all('span', {'itemprop': 'price'}):
                return item.attrs['content']

        elif self.website == "benqdirect":
            # Yikes this got ugly, but I don't care for this price because the Ebay one is cheaper
            # for item in soup.find_all('p', {'class': 'special-price'}):
            #     print item
            price = self.soup('p', {'class': 'special-price'})
            return price[0]('span')[1].text.replace("$", " ").strip()

        elif self.website == "acerrecertified":
            # I don't really care for the price of these. Just want to know when they're in stock
            for item in self.soup.find_all('span', {'id': 'unitprice'}):
                return item.text.replace("$", "")

    def getName(self):
        nameList = {"acer": "xg270hu", "asus": "mg278q", "benq": "xl2730z"}

        if self.website == "ebay":
            for name in nameList.keys():
                if name in str(self.soup.find('h1', {'itemprop': 'name'})).lower():
                    self.model = nameList[name]
                    return name

        elif self.website == "newegg":
            for name in nameList.keys():
                if name in str(self.soup.find('span', {'itemprop': 'name'})).lower():
                    self.model = nameList[name]
                    return name

        elif self.website == "benqdirect":
            self.model = nameList["benq"]
            return "benq"

        elif self.website == "acerrecertified":
            self.model = nameList["acer"]
            return "acer"

    def __str__(self):
        return "Website : {0}\n" \
               "Name    : {1}\n" \
               "Price   : {2}\n" \
               "Avail   : {3}\n" \
               "URL     : {4}\n".format(self.website,
                                        self.name + " " + self.model, self.price, self.available, self.url)


def main():
    print "----" * 3 + "\nBenq XL2730Z\n" + "----" * 3
    monitorCache = {}
    for url in monitorURLs:
        newMonitor = Monitor(url)

        # If the monitor becomes available, add it to cache or email me
        if newMonitor.available:
            # If monitor is not in cache, add the url and price to cache
            if newMonitor.url not in monitorCache:
                monitorCache[newMonitor.url] = newMonitor.price
                # If the monitor is Acer, immediately email me
                # Make sure the website isn't NewEgg because they're always in stock w/ bad price
                if newMonitor.name == "acer" and newMonitor.website != "newegg":
                    print "email me"
                    # TODO If monitor is Acer, then email me immediately
            # Else, if the monitor is in cache, check if current price was lowered
            else:
                # If current price is lower than one in cache, email me and replace price in cache
                if float(newMonitor.price) < float(monBenq[newMonitor.url]):
                    monitorCache[newMonitor.url] = newMonitor.price
                    # TODO: Notify via email that there's a new lowest price
            # print newMonitor.__str__()
        else:
            if newMonitor.url in monitorCache:
                del monitorCache[newMonitor.url]
        print newMonitor.__str__()

while True:
    main()
    print "\nSleeping for 5 minutes"
    time.sleep(300)
    print "=-=-=-=-=-=-" * 3




