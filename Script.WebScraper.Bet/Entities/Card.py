from Entities.Event import Event
from Entities.Fighter import Fighter

class Card:
    def __init__(self, eventTime="", cardType=""):
        self.eventTime = eventTime
        self.cardType = cardType
        self.cardEvents = []
    def printEvents(self):
        stringOfEvents = ""
        for card in self.cardEvents:
            stringOfEvents += str(card)
        return stringOfEvents
    def __str__(self):
        # return f"\n\tCard Type: {self.cardType}, Event Time: {self.eventTime}"
        return f"\n\tCard Type: {self.cardType}, Event Time: {self.eventTime}\n{self.printEvents()}"