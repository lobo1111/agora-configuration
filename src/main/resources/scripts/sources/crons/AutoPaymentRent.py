from pl.reaper.container.data import PaymentRent
from pl.reaper.container.data import PaymentRentDetails
from base.Container import Container
from entities.Dictionary import DictionaryManager
from entities.Account import AccountManager

class CronAutoPaymentRent(Container):
    
    def __init__(self):
        self._dictManager = DictionaryManager()
        self._dictManager.setSvars(self._svars)
        self._dictManager.setEntityManager(self._entityManager)
    
    def processDocuments(self):
        self._logger.info('Cron auto payment started...')
        self._documents = self.getDocuments()
        self._logger.info('Found %s documents ready for processing' % (str(self._documents.size())))
        for document in self._documents:
            self.handleDocument(document)
        self._logger.info('Cron auto payment finished.')
        
    def getDocuments(self):
        sql = "Select doc From IncomingPaymentDocumentPosition doc Join doc.status st Where st.key in('NEW', 'UNKNOWN')"
        return self._entityManager.createQuery(sql).getResultList()
    
    def handleDocument(self, document):
        possession = self.matchAutoPayment(document)
        if possession is None:
            self.setAsUnknown(document)
        else:  
            self.createPaymentRentFromDocument(document, possession)
            self.setAsProcessed(document)
        self._entityManager.persist(document)
        
    def matchAutoPayment(self, document):
        try:
            sql = "Select p From Possession p Join p.account account Where account.number = '%s'" % str(document.getClientNumber())
            return self._entityManager.createQuery(sql).getSingleResult()
        except:
            return None;
        
    def setAsUnknown(self, document):
        status = self._dictManager.findDictionaryInstance('DOCUMENT_STATUS', 'UNKNOWN')
        document.setStatus(status)
    
    def setAsProcessed(self, document):
        status = self._dictManager.findDictionaryInstance('DOCUMENT_STATUS', 'PROCESSED')
        document.setStatus(status)
        
    def createPaymentRentFromDocument(self, document, possession):
        paymentRent = PaymentRent()
        paymentRentDetails = PaymentRentDetails()
        paymentRent.setPaymentRentDetails(paymentRentDetails)
        paymentRentDetails.setPaymentRent(paymentRent)
        paymentRent.setMonth(self.getCurrentMonth())
        paymentRent.setBookingPeriod(self.getBookingPeriod())
        paymentRent.setPossession(possession)
        paymentRentDetails.setAccount(self.findAccountByNumber(document.getClientNumber()))
        paymentRentDetails.setClientName(document.getClientName())
        paymentRentDetails.setTitle(document.getTitle())
        paymentRentDetails.setBookingDate(document.getBookingDate())
        paymentRentDetails.setRequestDate(document.getRequestDate())
        paymentRentDetails.setValue(document.getIncome().floatValue())
        paymentRentDetails.setAuto(True)
        self._entityManager.persist(paymentRent)
    
    def findAccountByNumber(self, number):
        account = AccountManager()
        account.setEntityManager(self._entityManager)
        account.setSvars(self._svars)
        return account.findAccountByNumber(number)
    
    def getCurrentMonth(self):
        return self._entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()
    
    def getBookingPeriod(self):
        return self._entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()
    