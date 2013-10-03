from pl.reaper.container.data import PaymentRent

class CronAutoPaymentRent(Container):
    _logger = Logger([:_scriptId])
    
    def __init__(self):
        self._dictManager = DictionaryManager()
    
    def processDocuments(self):
        self._logger.info('Cron auto payment started...')
        self._documents = self.getDocuments()
        self._logger.info('Found %s documents ready for processing' % (str(self._documents.size())))
        for document in self._documents:
            self.handleDocument(document)
        self._logger.info('Cron auto payment finished.')
        
    def getDocuments(self):
        sql = "Select doc From IncomingPaymentDocumentPosition doc Join doc.status st Where st.key in('NEW', 'UNKNOWN')"
        return entityManager.createQuery(sql).getResultList()
    
    def handleDocument(self, document):
        possession = self.matchAutoPayment(document)
        if possession is None:
            self.setAsUnknown(document)
        else:  
            self.createPaymentRentFromDocument(document, possession)
            self.setAsProcessed(document)
        entityManager.persist(document)
        
    def matchAutoPayment(self, document):
        try:
            sql = "Select p From Possession p Join p.account account Where account.number = '%s'" % str(document.getClientNumber())
            return entityManager.createQuery(sql).getSingleResult()
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
        paymentRentDetails.setValue(document.getIncome())
        paymentRentDetails.setAuto(True)
        entityManager.persist(paymentRent)
    
    def findAccountByNumber(self, number):
        return AccountManager().findAccountByNumber(number)
    
    def getCurrentMonth(self):
        return entityManager.createQuery('SELECT dict.value FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = "PERIODS" AND dict.key = "CURRENT"').getSingleResult()
    
    def getBookingPeriod(self):
        return entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()
    