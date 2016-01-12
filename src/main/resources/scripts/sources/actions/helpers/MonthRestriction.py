from actions.helpers.Restriction import Restriction
from entities.BookingPeriod import BookingPeriodManager

class MonthRestriction(Restriction):
    
    def calculate(self):
        if int(BookingPeriodManager().getCurrentMonth()) < 12:
           self._result = True
        else:
            self._message = "To juz jest ostatni miesiac rozliczeniowy, nalezy wykonac zamkniecie roku"
            self._result = False
        
    def getTemplateName(self):
        return "month"
    