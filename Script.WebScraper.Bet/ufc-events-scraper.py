
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

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

TEST_MODE_ACTIVE=os.getenv('TEST_MODE')
CHROME_DRIVER_PATH=os.getenv('CHROME_DRIVER_PATH')
UFC_EVENTS_PAGE=os.getenv('UFC_EVENTS_PAGE')

clear = lambda: os.system('cls')
clear()

eventTypes = {
    "Main": "Main Card",
    "Preliminary": "Preliminary Card",
    "EarlyPreliminary": "Early Prelims"
}

ufcEventsList = []
ufcEventLinks = []

# ========= On Events Page - Reads all upcoming events =====================
if TEST_MODE_ACTIVE == "True":
    with open("./downloadedHTMLPages/Events_Page.html", encoding='utf8') as file:
        eventsPage = BeautifulSoup(file, "html.parser") 
else:
    result = requests.get(UFC_EVENTS_PAGE)
    eventsPage = BeautifulSoup(result.text, "html.parser")

eventsPage.prettify("utf-8")

eventsList = eventsPage.find_all("li", class_="l-listing__item")

for index, eventListItem in enumerate(eventsList):
    if index == 2 : break
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

if TEST_MODE_ACTIVE == "True":
    ufcEventLinks = ["./downloadedHTMLPages/FightNight_FontvsVera.html","./downloadedHTMLPages/UFC274_OliveiravsGaethje.html"]
    # ufcEventLinks = ["./mockHTMLPages/Fight_Night_1_Page.html","./mockHTMLPages/Fight_Night_2_Page.html","./mockHTMLPages/Main_Card_Page.html"]

# print(ufcEventLinks)
    # print(link)
    # print(f"eventName: {eventName}")
    # print(f"eventDate: {eventDate}")
    # print(f"eventVenue: {eventVenue}\n")

for eventIndex, ufcEventLink in enumerate(ufcEventLinks):
    if TEST_MODE_ACTIVE == "True":
        with open(ufcEventLink, encoding='utf8') as file:
            eventPage = BeautifulSoup(file, "html.parser")
    else:
        result = requests.get(ufcEventLink)
        eventPage = BeautifulSoup(result.text, "html.parser")

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

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(ufcEventLink)

    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH,"//*[@title='Accept Cookies Button']"))).click()
    xButton = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//*[@title='Accept Cookies Button']"))
    # xButton.click()
    driver.execute_script("arguments[0].click();", xButton)

    eventsList = buildEvents(eventPage, fighterList)
    # for event in eventsList:
    #     print(event)

    ufcEventsList[eventIndex].eventCards[0].cardEvents = eventsList

    if TEST_MODE_ACTIVE == "False":
        driver.quit()

for ufcEvent in ufcEventsList:
    print(ufcEvent)
    # ufcEvent.printCards()
    print()
