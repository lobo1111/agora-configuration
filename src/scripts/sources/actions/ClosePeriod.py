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
        chargingsRestriction = ChargingRestriction().calculate()
        monthRestriction = MonthRestriction().calculate()
        yearRestriction = YearRestriction().calculate()
        self._logger.info('Invoice restriction: %s' % str(invoiceRestriction))
        self._logger.info('Chargings restriction: %s' % str(chargingsRestriction))
        self._logger.info('Month restriction: %s' % str(monthRestriction))
        self._logger.info('Year restriction: %s' % str(yearRestriction))
        if invoiceRestriction and chargingsRestriction and (yearRestriction or monthRestriction):
            DocumentManager().bookAll()
            self._logger.info('All documents booked')
            if monthRestriction:
                self.setNextMonth()
                self._logger.info('Month closed')
            elif yearRestriction:
                BookingPeriodManager().closeYear()
                self._logger.info('Year closed')
        self._svars.put('output', '-1')
            
    def setNextMonth(self):
        self._nextMonth = int(BookingPeriodManager().getCurrentMonth().getValue()) + 1
        dict = DictionaryManager().findDictionaryInstance("PERIODS", "CURRENT")
        dict.setValue(str(self._nextMonth))
        self.saveEntity(dict)
    