from base.Container import Container
from entities.Dictionary import DictionaryManager
from actions.ChargingBooker import ChargingBooker
from actions.PaymentBooker import PaymentBooker
from actions.InvoiceBooker import InvoiceBooker
from actions.BankNoteBooker import BankNoteBooker
from actions.BankCreditBooker import BankCreditBooker
from actions.AccountProvisionBooker import AccountProvisionBooker

class Close(Container):
    
    def closeMonth(self):
        self._currentMonth = int(self.getCurrentMonth())
        if self._currentMonth < 12:
            self._logger.info('Closing month...')
            self.clearQueue()
            self.bookAll()
            self.setNextMonth()
            self._logger.info('Month closed')
        else:
            self._logger.info("Month can't be closed - its already %d" % self._currentMonth)
        
    def getCurrentMonth(self):
        return self._entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()
        
    def clearQueue(self):
        self._entityManager.createQuery("Delete From ChargingQueue cq").executeUpdate()
        self._logger.info('Charge queue cleared')
        
    def setNextMonth(self):
        self._currentMonth += 1
        manager = DictionaryManager()
        manager.setSvars(self._svars)
        manager.setEntityManager(self._entityManager)
        dict = manager.findDictionaryInstance("PERIODS", "CURRENT")
        dict.setValue(str(self._currentMonth))
        self._entityManager.persist(dict)
        self._entityManager.flush()
        
    def bookAll(self):
        cBooker = ChargingBooker()
        cBooker.bookAllChargings()
        pBooker = PaymentBooker()
        pBooker.bookAllPayments()
        iBooker = InvoiceBooker()
        iBooker.bookAllInvoices()
        nBooker = BankNoteBooker()
        nBooker.bookAllNotes()
        bcBooker = BankCreditBooker()
        bcBooker.bookAllCredits()
        apBooker = AccountProvisionBooker()
        apBooker.bookAllProvisions()