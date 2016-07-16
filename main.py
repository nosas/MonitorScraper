from monitorList import monitorURLs
from monitorClass import Monitor
from login import gmail_login
import email
import time


def main():
    print "----" * 3 + "\nBenq XL2730Z\n" + "----" * 3
    # TODO Read/write cache from file
    monitorCache = {}
    gmail = gmail_login()
    to_email = ["sasonreza@gmail.com"]

    for url in monitorURLs:
        newMonitor = Monitor(url)

        # If the monitor is available, add it to cache or email me
        if newMonitor.available:
            # If monitor is not in cache, add the url and price to cache
            if newMonitor.url not in monitorCache:
                monitorCache[newMonitor.url] = newMonitor.price
                # If the monitor is Acer, immediately email me
                # Make sure the website isn't NewEgg because they're always in stock w/ bad price
                if newMonitor.name == "acer" and newMonitor.website != "newegg":
                    sendMail(gmail, to_email, newMonitor.name, newMonitor.url)
            # Else, the monitor is in cache, so check if current price was lowered
            else:
                # If current price is lower than one in cache, email me and replace price in cache
                if float(newMonitor.price) < float(monitorCache[newMonitor.url]):
                    monitorCache[newMonitor.url] = newMonitor.price
                    sendMail(gmail, to_email, newMonitor.name, newMonitor.url)
            print newMonitor.__str__()
        # Else, the monitor is out of stock so remove it from the cache
        else:
            if newMonitor.url in monitorCache:
                del monitorCache[newMonitor.url]


def sendMail(from_email, to_email, subject, body):
    msg = email.message.Message()
    msg.set_payload(body)
    msg['Subject'] = subject
    from_email.send(msg, to_email)
    print "Email sent ##########"

while True:
    main()
    print "\nSleeping for 5 minutes"
    time.sleep(300)
    print "=-=-=-=-=-=-" * 3
