from monitorList import monitorURLs
from monitorClass import Monitor
import time


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
                if float(newMonitor.price) < float(monitorCache[newMonitor.url]):
                    monitorCache[newMonitor.url] = newMonitor.price
                    # TODO: Notify via email that there's a new lowest price
            print newMonitor.__str__()
        else:
            if newMonitor.url in monitorCache:
                del monitorCache[newMonitor.url]
        # print newMonitor.__str__()

while True:
    main()
    print "\nSleeping for 5 minutes"
    time.sleep(300)
    print "=-=-=-=-=-=-" * 3
