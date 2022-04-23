from Entities.Fighter import Fighter

class Event:
    def __init__(self, eventWeightClass="", eventFighter1=Fighter(), eventFighter2=Fighter()):
        self.eventWeightClass = eventWeightClass
        self.selectedFighter = ""
        self.eventFighter1 = eventFighter1
        self.eventFighter2 = eventFighter2
    def __str__(self):
     return f"\n\t\tEvent Weight Class: {self.eventWeightClass}\n\t\tSelected Fighter: {self.selectedFighter}\n\t\tEventFighter1: {self.eventFighter1}\n\t\tEventFighter2: {self.eventFighter2}\n"