from actions.helpers.Restriction import Restriction
from structures.BookingPeriod import BookingPeriodManager

class YearRestriction(Restriction):
    
    def calculate(self):
        return (int(BookingPeriodManager().getCurrentMonth().getValue()) == 12)
    