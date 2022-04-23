class Fighter(object):
    def __init__(self, fighterName="", fighterRecord="", fighterImage=""):
        self.fighterName = fighterName
        self.fighterRecord = fighterRecord
        self.fighterImage = fighterImage
    def __str__(self):
     return f"Fighter Name: {self.fighterName}, Fighter Record: {self.fighterRecord}, Fighter Image: {self.fighterImage}"