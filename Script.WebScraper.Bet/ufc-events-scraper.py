
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup

class Fighter(object):
    def __init__(self, fighterName, fighterRecord, fighterImage):
        self.fighterName = fighterName
        self.fighterRecord = fighterRecord
        self.fighterImage = fighterImage

class Event:
    def __init__(self, eventWeightClass, selectedFighter, eventFighter1, eventFighter2):
        self.eventWeightClass = eventWeightClass
        self.selectedFighter = selectedFighter
        self.eventFighter1 = eventFighter1
        self.eventFighter2 = eventFighter2

class Card:
    def __init__(self, eventTime, cardType):
        self.eventTime = eventTime
        self.cardType = cardType
        self.cardEvents = []

class UFCEvent:
    def __init__(self, eventName, eventDate, eventVenue, eventCards):
        self.eventName = eventName
        self.eventDate = eventDate
        self.eventVenue = eventVenue
        self.eventCards = []

# ========= Pulling from website =====================
# url = "https://www.ufc.com/event/ufc-274"

# result = requests.get(url)
# eventPage = BeautifulSoup(result.text, "html.parser")

# ========= Writing html to file =====================
# url = "https://www.ufc.com/event/ufc-274"

# result = requests.get(url)
# doc = BeautifulSoup(result.text, "html.parser")
# html = doc.prettify("utf-8")

# with open("Main_Card_Page.html", "wb") as file:
#     file.write(html)

# ========= Read Locally =====================
# print(doc.prettify())
        
# with is short-form way to work with files with a built in error handler
#with open("UFC 274 _ Oliveira vs Gaethje _ UFC.html", "r") as file:
    # use BeautifulSoup constructore to pass in the html file and use a specific parser
    #doc = BeautifulSoup(file, "html.parser") 

ufcEventsList = []

# ========= On Events Page - Reads all upcoming events =====================
with open("Events_Page.html", encoding='utf8') as file:
    eventsPage = BeautifulSoup(file, "html.parser") 

eventsPage.prettify("utf-8")

eventsList = eventsPage.find_all("li", class_="l-listing__item")

for index, eventListItem in enumerate(eventsList):
    if index == 3 : break
    linkDiv = eventsList[index].find("h3", class_="c-card-event--result__headline")
    linkHrefEl = linkDiv.find("a", href=re.compile("/event/ufc"))
    link = f"https://www.ufc.com{linkHrefEl.get('href')}"

    eventType = ""
    matchUp = linkHrefEl.getText().strip()

    if "fight-night" in link:
        eventType = "Fight Night"
    elif "ufc" in link:
        stringArray = link.split("-")
        eventNumber = stringArray[len(stringArray) - 1]
        eventType = f"UFC {eventNumber}"
    else:
        print("no event found")    

    dateDiv = eventsList[index].find("div", class_="c-card-event--result__date tz-change-data")
    timeStampMain = dateDiv.get("data-main-card-timestamp")

    date = "N/A"

    if timeStampMain != "":
        dateTime = datetime.fromtimestamp(int(timeStampMain))
        date = str(dateTime).replace(" ", "T")
        timeMain = datetime.fromtimestamp(int(timeStampMain)).strftime('%#I%p')
        #print(f"timeMain: {timeMain}")

    timeStampPrelims = dateDiv.get("data-prelims-card-timestamp")
    if timeStampPrelims != '':
        timePrelims = datetime.fromtimestamp(int(timeStampPrelims)).strftime('%#I%p')
        #print(f"timePrelims: {timePrelims}")

    timeStampEarlyPrelims = dateDiv.get("data-early-card-timestamp")
    if timeStampEarlyPrelims != '':
        timeEarlyPrelims = datetime.fromtimestamp(int(timeStampEarlyPrelims)).strftime('%#I%p')
        #print(f"timeEarlyPrelims: {timeEarlyPrelims}")

    venueDiv = eventsList[index].find("div", class_="field field--name-taxonomy-term-title field--type-ds field--label-hidden field__item")
    venue = venueDiv.getText().strip()

    eventName = f"{eventType} - {matchUp}"
    eventDate = date 
    eventVenue = venue

    print(link)
    print(f"eventName: {eventName}")
    print(f"eventDate: {eventDate}")
    print(f"eventVenue: {eventVenue}\n")

# ========= On Event Page - Reads all fighters from event =====================

def buildFighters(eventPage):
    fightEvents = eventPage.find_all("li", class_="l-listing__item")
    fighterNamesList = getFighterNames(fightEvents)
    print(fighterNamesList)
    fighterImageList = getFighterImages(fightEvents)
    print(fighterImageList)

def getFighterNames(fightEvents):
    fighterNamesList = []
    for fightEvent in fightEvents:
        matchUpDiv = fightEvent.find_all("div", class_="c-listing-fight__corner-name")
        fighter1Div = matchUpDiv[0]
        fighter2Div = matchUpDiv[1]

        fighter1Names = fighter1Div.find_all("span")
        fighter2Names = fighter2Div.find_all("span")

        if not fighter1Names:
            fighterNamesList.append(fighter1Div.getText().strip())
            # print(fighter1Div.getText().strip())
        else:   
            fullName = ""
            for name in fighter1Names:
                fullName += f"{name.getText()} "
            fighterNamesList.append(fullName.strip())
            # print(fullName.strip())
        
        if not fighter2Names:
            fighterNamesList.append(fighter2Div.getText().strip())
            # print(fighter2Div.getText().strip())
        else:   
            fullName = ""
            for name in fighter2Names:
                fullName += f"{name.getText()} "
            fighterNamesList.append(fullName.strip())
            # print(fullName.strip())

        # print()
    return fighterNamesList

def getFighterImages(fightEvents):
    fighterImageList = []
    for fightEvent in fightEvents:
        fighterImages = fightEvent.find_all("img", class_="image-style-event-fight-card-upper-body-of-standing-athlete")
        for image in fighterImages:
            fighterImageList.append(image['src'])
            # print(image['src'])
    return fighterImageList

#buildFighters(eventPage)