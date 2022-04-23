
from datetime import datetime
import re
import requests
from bs4 import BeautifulSoup

import os
from dotenv import load_dotenv

from Factories.FighterFactory import *
from Factories.EventFactory import *

from Entities.Card import Card
from Entities.Event import Event
from Entities.Fighter import Fighter
from Entities.UFCEvent import UFCEvent

load_dotenv()

TEST_MODE_ACTIVE=os.getenv('TEST_MODE')

eventTypes = {
    "Main": "Main Card",
    "Preliminary": "Preliminary Card",
    "EarlyPreliminary": "Early Prelims"
}

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
ufcEventLinks = []

clear = lambda: os.system('cls')
clear()

# ========= On Events Page - Reads all upcoming events =====================
# with open("./mockHTMLPages/Events_Page.html", encoding='utf8') as file:
#     eventsPage = BeautifulSoup(file, "html.parser") 
with open("./downloadedHTMLPages/Events_Page.html", encoding='utf8') as file:
    eventsPage = BeautifulSoup(file, "html.parser") 

eventsPage.prettify("utf-8")

eventsList = eventsPage.find_all("li", class_="l-listing__item")

for index, eventListItem in enumerate(eventsList):
    if index == 3 : break
    linkDiv = eventsList[index].find("h3", class_="c-card-event--result__headline")
    linkHrefEl = linkDiv.find("a", href=re.compile("/event/ufc"))
    link = f"https://www.ufc.com{linkHrefEl.get('href')}"
    ufcEventLinks.append(link)

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

    listCardPerEvent = []

    if timeStampMain != "":
        dateTime = datetime.fromtimestamp(int(timeStampMain))
        date = str(dateTime).replace(" ", "T")
        timeMain = datetime.fromtimestamp(int(timeStampMain)).strftime('%#I%p')
        mainCard = Card(timeMain, eventTypes["Main"])
        listCardPerEvent.append(mainCard)
        #print(f"timeMain: {timeMain}")

    timeStampPrelims = dateDiv.get("data-prelims-card-timestamp")
    if timeStampPrelims != '':
        timePrelims = datetime.fromtimestamp(int(timeStampPrelims)).strftime('%#I%p')
        prelimCard = Card(timePrelims, eventTypes["Preliminary"])
        listCardPerEvent.append(prelimCard)
        #print(f"timePrelims: {timePrelims}")

    timeStampEarlyPrelims = dateDiv.get("data-early-card-timestamp")
    if timeStampEarlyPrelims != '':
        timeEarlyPrelims = datetime.fromtimestamp(int(timeStampEarlyPrelims)).strftime('%#I%p')
        earlyPrelimCard = Card(timeEarlyPrelims, eventTypes["EarlyPreliminary"])
        listCardPerEvent.append(earlyPrelimCard)
        #print(f"timeEarlyPrelims: {timeEarlyPrelims}")

    venueDiv = eventsList[index].find("div", class_="field field--name-taxonomy-term-title field--type-ds field--label-hidden field__item")
    venue = venueDiv.getText().strip()

    eventName = f"{eventType} - {matchUp}"
    eventDate = date 
    eventVenue = venue

    ufcEvent = UFCEvent(eventName, eventDate, eventVenue)

    for card in listCardPerEvent:
        ufcEvent.eventCards.append(card)
        #print(card)

    ufcEventsList.append(ufcEvent)

# for ufcEvent in ufcEventsList:
#     print(ufcEvent)
#     # ufcEvent.printCards()
#     print()

if TEST_MODE_ACTIVE:
    ufcEventLinks = ["./downloadedHTMLPages/FightNight_LemosvsAndrade.html","./downloadedHTMLPages/FightNight_FontvsVera.html","./downloadedHTMLPages/UFC274_OliveiravsGaethje.html"]
    # ufcEventLinks = ["./mockHTMLPages/Fight_Night_1_Page.html","./mockHTMLPages/Fight_Night_2_Page.html","./mockHTMLPages/Main_Card_Page.html"]

# print(ufcEventLinks)
    # print(link)
    # print(f"eventName: {eventName}")
    # print(f"eventDate: {eventDate}")
    # print(f"eventVenue: {eventVenue}\n")

for eventIndex, ufcEventLink in enumerate(ufcEventLinks):
    # ========= On Events Page - Reads all upcoming events =====================
    with open(ufcEventLink, encoding='utf8') as file:
        eventPage = BeautifulSoup(file, "html.parser") 

    eventPage.prettify("utf-8")

    cardList = eventPage.find("ul", class_="horizontal-tabs-list")
    cardTabs = cardList.find_all("li")

    listCards = []

    for tab in cardTabs:
        # if style display none is applied, it is not an included event card
        if tab.has_attr('style'):
            None
            #print(tab.find("strong").getText().strip())
        else:
            listCards.append(tab.find("strong").getText().strip())

    # cardEventsDiv = eventPage.find("div", class_="c-listing__wrapper--horizontal-tabs")
    # cardEventsTabs = cardEventsDiv.find_all("details")

    # print(cardEventsTabs)

    # ========= On Event Page - Reads all fighters from event =====================
    # print(listCards)
    # print(ufcEventsList[eventIndex].eventCards[0])

    # TODO: This only works for main card right now. Make it work for all cards.
    fighterList = buildFighters(eventPage)
    # for fighter in fighterList:
    #     print(fighter)
    eventsList = buildEvents(eventPage, fighterList)
    # for event in eventsList:
    #     print(event)

    ufcEventsList[eventIndex].eventCards[0].cardEvents = eventsList

for ufcEvent in ufcEventsList:
    print(ufcEvent)
    # ufcEvent.printCards()
    print()