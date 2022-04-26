from Entities.Event import Event

def buildEvents(eventPage, fighterList, fighterIndexStart, fighterIndexEnd):
    fightEvents = eventPage.find_all("li", class_="l-listing__item")
    weightClassList = getFighterWeightClass(fightEvents)
    eventList = []

    weightClassIndex = 0

    for fighterIndex in range(fighterIndexStart,fighterIndexEnd,2):
        eventList.append(Event(weightClassList[weightClassIndex], fighterList[fighterIndex], fighterList[fighterIndex+1]))
        weightClassIndex += 1

    # print(weightClassList)
    # print(fighterList)
    # for event in eventList:
    #     print(event)
    return eventList

def getFighterWeightClass(fightEvents):
    fighterWeightClassList = []
    for fightEvent in fightEvents:
        fighterWeightClasss = fightEvent.find("div", class_="c-listing-fight__class")
        fighterWeightClassList.append(fighterWeightClasss.getText().strip())
    return fighterWeightClassList