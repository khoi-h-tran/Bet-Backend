from Entities.Event import Event

def buildEvents(eventPage, fighterList):
    fightEvents = eventPage.find_all("li", class_="l-listing__item")
    weightClassList = getFighterWeightClass(fightEvents)
    eventList = []

    weightClassIndex = 0

    for fighterIndex in range(0,len(fighterList),2):
        eventList.append(Event(weightClassList[weightClassIndex], fighterList[fighterIndex], fighterList[fighterIndex+1]))
        weightClassIndex += 1

    # print(weightClassList)
    # print(fighterList)
    return eventList

def getFighterWeightClass(fightEvents):
    fighterWeightClassList = []
    for fightEvent in fightEvents:
        fighterWeightClasss = fightEvent.find("div", class_="c-listing-fight__class")
        fighterWeightClassList.append(fighterWeightClasss.getText().strip())
    return fighterWeightClassList