from bs4 import *
from urllib import urlopen


# Retrieving NewEgg data is tough, so I had to pull the json data from the page
# and parse the product_instock variable from it
def getNeweggData(soup):
        lineIndex = 0
        startIndex = 0
        soupSplit = soup.text.splitlines()
        itemData = "{"

        while lineIndex < len(soupSplit):
            currentLine = soupSplit[lineIndex]

            # If the beginning of utag_data has been found, append the following lines and break once end of var
            if startIndex != 0:
                itemData += currentLine.lstrip()
                if "}" in currentLine:
                    break
            elif "var utag_data = {" in currentLine:
                startIndex = lineIndex

            lineIndex += 1

        return itemData


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
        elif self.website == "newegg":
            itemData = getNeweggData(self.soup)
            for item in itemData.split(","):
                if "product_instock" in item:
                    # If there's a 0, that means it's out of stock
                    if "0" in item.split(":")[1][2]:
                        return False
                    break

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

        elif self.website == "newegg":
            # <meta content="399.99" itemprop="price"/>
            for item in self.soup.find_all('meta', {'itemprop': 'price'}):
                return item['content']

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
                                        str(self.name) + " " + str(self.model), self.price, self.available, self.url)






