
from datetime import datetime
from pprint import pprint
import re
import requests
from bs4 import BeautifulSoup

import os
from dotenv import load_dotenv

from Factories.FighterFactory import *
from Factories.EventFactory import *

from Entities.Card import Card
from Entities.Card import CardSchema
from Entities.Event import Event
from Entities.Event import EventSchema
from Entities.Fighter import Fighter
from Entities.Fighter import FighterSchema
from Entities.UFCEvent import UFCEvent
from Entities.UFCEvent import UFCEventSchema
from Entities.UFCEvent import UFCEventsListSchema

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import pyrebase
from Firebase.Config import config

import json

load_dotenv()

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
result = requests.get(UFC_EVENTS_PAGE)
eventsPage = BeautifulSoup(result.text, "html.parser")

eventsPage.prettify("utf-8")

eventsList = eventsPage.find_all("li", class_="l-listing__item")

for index, eventListItem in enumerate(eventsList):
    if index == 1 : break
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

for eventIndex, ufcEventLink in enumerate(ufcEventLinks):
    result = requests.get(ufcEventLink)
    eventPage = BeautifulSoup(result.text, "html.parser")

    eventPage.prettify("utf-8")
    
    # Finding how many fighters are in each card
    fighterCountPerCard = []
    # cardEventsDiv = eventPage.find_all("div", class_="details-wrapper")
    # cardEventsDiv = eventPage.find_all("ul", class_="l-listing__group--bordered")
    # cardEventsDiv = eventPage.find_all("details")
    cardEventsDiv = eventPage.find_all("ul", class_="l-listing__group--bordered")
    # print(f"cardEventsDiv {len(cardEventsDiv)}")
    for cardEventDiv in cardEventsDiv:
        fighterListItems = cardEventDiv.find_all("li")
        # print(f"fighterListItems {len(fighterListItems)}")
        if len(fighterListItems) > 0:
            # multiplied by 2 because list items is each matchup, so a fighter count would be 2x
            fighterCountPerCard.append(len(fighterListItems)*2)

    fighterList = buildFighters(eventPage)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get(ufcEventLink)

    acceptButton = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.XPATH, "//*[@title='Accept Cookies Button']"))
    driver.execute_script("arguments[0].click();", acceptButton)

    matchUps = WebDriverWait(driver, timeout=10).until(lambda d: d.find_elements(By.CLASS_NAME, "c-listing-fight"))

    fighter1RecordList = []
    fighter2RecordList = []

    for matchUp in matchUps:
        driver.execute_script("arguments[0].click();", matchUp)

        iframe = WebDriverWait(driver, timeout=10).until(lambda d: d.find_element(By.ID, "matchup-modal-content"))
        driver.switch_to.frame(iframe)

        fighter1Record = driver.find_element(By.CSS_SELECTOR, ".c-stat-compare__group-1.red")
        fighter1RecordList.append(fighter1Record.get_attribute('innerHTML').strip())

        fighter2Record = driver.find_element(By.CSS_SELECTOR, ".c-stat-compare__group-2.blue")
        fighter2RecordList.append(fighter2Record.get_attribute('innerHTML').strip())

        driver.switch_to.default_content()

    fighterRecordIndex = 0

    for fighterIndex in range(0, len(fighterList), 2):
        fighterList[fighterIndex].fighterRecord = fighter1RecordList[fighterRecordIndex]
        fighterList[fighterIndex+1].fighterRecord = fighter2RecordList[fighterRecordIndex]
        fighterRecordIndex += 1

    startIndex = 0
    # print(fighterCountPerCard)
    for fightCardCountIndex, fighterCount in enumerate(fighterCountPerCard):
        endIndex = startIndex + fighterCount - 1
        eventsList = buildEvents(eventPage, fighterList, startIndex, endIndex)
        ufcEventsList[eventIndex].eventCards[fightCardCountIndex].cardEvents = eventsList
        startIndex += fighterCount

    # for fighter in fighterList:
    #     print(fighter)
    driver.quit()

jsonUFCEventsList = []

for ufcEvent in ufcEventsList:
    schemaUfcEvents = UFCEventSchema()
    jsonResult = schemaUfcEvents.dump(ufcEvent)
    jsonUFCEventsList.append(jsonResult)

firebase = pyrebase.initialize_app(config)
db = firebase.database()
db.set(jsonUFCEventsList)

# for ufcEvent in ufcEventsList:
#     print(ufcEvent)
#     # ufcEvent.printCards()
#     print()
