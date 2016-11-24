from base.Container import Container
from structures.BookingPeriod import BookingPeriodManager
from structures.Dictionary import DictionaryManager
from documents.Document import DocumentManager
from actions.helpers.ChargingRestriction import ChargingRestriction
from actions.helpers.MonthRestriction import MonthRestriction
from actions.helpers.YearRestriction import YearRestriction
from actions.helpers.InvoiceRestriction import InvoiceRestriction

class ClosePeriodManager(Container):

    def close(self):
        invoiceRestriction = InvoiceRestriction().calculate()
        chargingRestriction = ChargingRestriction().calculate()
        monthRestriction = MonthRestriction().calculate()
        yearRestriction = YearRestriction().calculate()
        if invoiceRestriction and chargingsRestriction and (yearRestriction or monthRestriction):
            DocumentManager().bookAll()
            if monthRestriction:
                self.setNextMonth()
            elif yearRestriction:
                BookingPeriodManager().closeYear()
            
    def setNextMonth(self):
        self._nextMonth = int(BookingPeriodManager().getCurrentMonth()) + 1
        dict = DictionaryManager().findDictionaryInstance("PERIODS", "CURRENT")
        dict.setValue(str(self._nextMonth))
        self.saveEntity(dict)
    