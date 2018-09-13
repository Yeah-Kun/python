class Park:
    def __init__(self,weekdays,adult,kid):
        self.weekdays = int(weekdays)
        self.adult = float(adult)
        self.kid = float(kid)
    def weekday(self):
        self.weekday = (self.adult + self.kid * 0.5) * self.weekdays
        return self.weekday
    def weekend(self):
        self.weekend = (self.adult+ self.kid * 0.5) * self.weekdays * 1.2
        return self.weekend
