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

class UFCEvents:
    def __init__(self, eventName, eventDate, eventVenue, eventCards):
        self.eventName = eventName
        self.eventDate = eventDate
        self.eventVenue = eventVenue
        self.eventCards = []

url = "https://www.ufc.com/event/ufc-274"

result = requests.get(url)
doc = BeautifulSoup(result.text, "html.parser")
# print(doc.prettify())
        
# with is short-form way to work with files with a built in error handler
#with open("UFC 274 _ Oliveira vs Gaethje _ UFC.html", "r") as file:
    # use BeautifulSoup constructore to pass in the html file and use a specific parser
    #doc = BeautifulSoup(file, "html.parser") 

ufcEventsList = []

def buildFighters(doc):
    fightEvents = doc.find_all("li", class_="l-listing__item")
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

buildFighters(doc)