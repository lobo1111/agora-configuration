class CronAutoPayment(Container):
    _logger = Logger([:_scriptId])
    
    def __init__(self):
        self._logger.info('Cron auto payment started...')
        self._dictManager = DictionaryManager()
        self._documents = self.getDocuments()
        self._logger.info('Found %s documents ready for processing' % (str(self._documents.size())))
        for document in self._documents:
            self._logger.info('Processing document - id:%s' % document.getId())
            self.handleDocument(document)
            self._logger.info('Document processed')
        self._logger.info('Cron auto payment finished.')
        
    def getDocuments(self):
        sql = "Select doc From IncomingPaymentDocumentPosition doc Join doc.status st Where st.key in('NEW', 'UNKNOWN')"
        return entityManager.createQuery(sql).getResultList()
    
    def handleDocument(self, document):
        autoPayment = self.matchAutoPayment(document)
        if autoPayment is None:
            self._logger.info("Can't match this document to any account.")
            self.setAsUnknown(document)
        else:  
            self._logger.info("Document matched, creating payments....")
            self.createPayments(document, autoPayment)
            #self.setAsProcessed(document)
        entityManager.persist(document)
        
    def matchAutoPayment(self, document):
        try:
            sql = "Select auto From AutoPayment auto Join auto.account account Where account.number = '%s'" % str(document.getClientNumber())
            return entityManager.createQuery(sql).getSingleResult()
        except:
            return None;
        
    def setAsUnknown(self, document):
        status = self._dictManager.findDictionaryInstance('DOCUMENT_STATUS', 'UNKNOWN')
        document.setStatus(status)
    
    def setAsProcessed(self, document):
        status = self._dictManager.findDictionaryInstance('DOCUMENT_STATUS', 'PROCESSED')
        document.setStatus(status)
    
    def createPayments(self, documentPosition, autoPayment):
        income = documentPosition.getIncome().floatValue()
        self._logger.info("Processing position %s, with income %s" %(str(documentPosition.getId()), str(income)))
        for order in self.getOrders(autoPayment.getId()):
            zpk = order.getZpk()
            self._logger.info("Booking on %s..." % str(zpk.getNumber))
            if income > 0 and self.hasNegativeBalance(zpk):
                income = self.book(documentPosition, income, zpk)
            else:
                self._logger.info("It's already balanced")
        if income > 0:
            self._logger.info("Booking the rest on %s" % str(autoPayment.getZpk().getId()))
            self.book(documentPosition, income, autoPayment.getZpk())

    def getOrders(self, parentId):
        sql = "SELECT c FROM AutoPaymentOrder c JOIN c.autoPayment ap WHERE ap.id = %s ORDER BY c.order" % str(parentId)
        return entityManager.createQuery(sql).getResultList()

    def hasNegativeBalance(self, zpk):
        defaultPeriod = BookingPeriodManager().findDefaultBookingPeriod()
        balance = ZpkManager().findBalanceByZpkAndPeriod(zpk, defaultPeriod)
        return (balance.getCredit() - balance.getDebit()) < 0

    def book(self, documentPosition, income, zpk):
        pass
        
        