from Entities.Card import Card
from Entities.Event import Event
from Entities.Fighter import Fighter

class UFCEvent:
    def __init__(self, eventName="", eventDate="", eventVenue=""):
        self.eventName = eventName
        self.eventDate = eventDate
        self.eventVenue = eventVenue
        self.eventCards = []
    def printCards(self):
        stringOfCards = ""
        for card in self.eventCards:
            stringOfCards += str(card)
        return stringOfCards
    def __str__(self):
     return f"Event Name: {self.eventName}\nEvent Date: {self.eventDate}\nEvent Venue: {self.eventVenue}\nEvent Cards: {self.printCards()}"