from actions.helpers.Restriction import Restriction
from entities.BookingPeriod import BookingPeriodManager

class YearRestriction(Restriction):
    
    def calculate(self):
        if int(BookingPeriodManager().getCurrentMonth()) == 12:
           self._result = True
           self._message = "Zaakceptowany"
        else:
            self._message = "Rok mozna zamknac tylko w 12 miesiacu rozliczeniowym"
            self._result = False
        
    def getTemplateName(self):
        return "year"
    