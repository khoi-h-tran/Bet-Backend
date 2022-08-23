from Entities.Fighter import Fighter

def buildFighters(eventPage):
    fightEvents = eventPage.find_all("li", class_="l-listing__item")
    fighterNamesList = getFighterNames(fightEvents)
    fighterImageList = getFighterImages(fightEvents)
    fighterList = []
    for fighterIndex, fighterName in enumerate(fighterNamesList):
        fighterList.append(Fighter(fighterName,"",fighterImageList[fighterIndex]))
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
        else:   
            fullName = ""
            for name in fighter1Names:
                fullName += f"{name.getText().strip()} "
            fighterNamesList.append(fullName.strip())
        
        if not fighter2Names:
            fighterNamesList.append(fighter2Div.getText().strip())
        else:   
            fullName = ""
            for name in fighter2Names:
                fullName += f"{name.getText().strip()} "
            fighterNamesList.append(fullName.strip())

    return fighterNamesList

def getFighterImages(fightEvents):
    fighterImageList = []
    for fightEvent in fightEvents:
        fighterImages = fightEvent.find_all("img")
        for image in fighterImages:
            fighterImageList.append(image['src'])
    # Remove the flags of the fighter's nation from the image list (only want to keep figher images)
    fighterImageList = [ image for image in fighterImageList if "flag" not in image ]
    blankImage = 'data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAIBRAA7'
    fighterImageList = [ blankImage if "silhouette" in image else image for image in fighterImageList ]
    print(len(fighterImageList))
    print(fighterImageList)

    return fighterImageList