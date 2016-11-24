from actions.helpers.Restriction import Restriction
from entities.BookingPeriod import BookingPeriodManager

class YearRestriction(Restriction):
    
    def calculate(self):
        self._result = (int(BookingPeriodManager().getCurrentMonth()) == 12)
    