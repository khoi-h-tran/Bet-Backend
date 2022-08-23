from Entities.Card import Card
from Entities.Card import CardSchema
from Entities.Event import Event
from Entities.Event import EventSchema
from Entities.Fighter import Fighter
from Entities.Fighter import FighterSchema

from marshmallow import Schema, fields

class UFCEvent:
    startColour = '\33[32m'
    endColour = '\033[0m'
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
     return f"{self.startColour}Event Name: {self.eventName}\nEvent Date: {self.eventDate}\nEvent Venue: {self.eventVenue}{self.endColour}\nEvent Cards: {self.printCards()}"

class UFCEventSchema(Schema):
    eventName = fields.Str()
    eventDate = fields.Str()
    eventVenue = fields.Str()
    eventCards = fields.List(fields.Nested(CardSchema), required=True)

# class UFCEventsListSchema(Schema):
#     ufcEvents = fields.List(fields.Nested(UFCEventSchema), required=True)