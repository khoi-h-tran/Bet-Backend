from Entities.Fighter import Fighter

def buildFighters(eventPage):
    fightEvents = eventPage.find_all("li", class_="l-listing__item")
    fighterNamesList = getFighterNames(fightEvents)
    #print(fighterNamesList)
    #fighterRecordList = getFighterRecords(fightEvents)
    #print(fighterRecordList)
    fighterImageList = getFighterImages(fightEvents)
    #print(fighterImageList)
    fighterList = []
    for fighterName in fighterNamesList:
        fighterList.append(Fighter(fighterName,"",""))
    # for fighter in fighterList:
    #     print(fighter)
    return fighterList

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
                fullName += f"{name.getText().strip()} "
            fighterNamesList.append(fullName.strip())
            #print(fullName.strip())
        
        if not fighter2Names:
            fighterNamesList.append(fighter2Div.getText().strip())
            # print(fighter2Div.getText().strip())
        else:   
            fullName = ""
            for name in fighter2Names:
                fullName += f"{name.getText().strip()} "
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