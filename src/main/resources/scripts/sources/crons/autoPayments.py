from pl.reaper.container.data import Payment

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
        possession = self.matchAutoPayment(document)
        if possession is None:
            self._logger.info("Can't match this document to any account.")
            self.setAsUnknown(document)
        else:  
            self._logger.info("Document matched, creating payments....")
            self.createPayments(document, possession)
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
    
    def createPayments(self, documentPosition, possession):
        income = documentPosition.getIncome().floatValue()
        self._logger.info("Processing position %s, with income %s" %(str(documentPosition.getId()), str(income)))
        for order in self.getOrders(possession.getId()):
            zpk = order.getZpk()
            vars.put(self._prefix + 'communityId', str(zpk.getCommunity().getId()))
            self._logger.info("Booking on %s..." % str(zpk.getNumber()))
            if income > 0 and self.hasNegativeBalance(zpk):
                income = self.book(documentPosition, income, zpk)
            else:
                self._logger.info("It's already balanced")
        if income > 0:
            self._logger.info("Booking the rest on %s" % str(possession.getDefaultBooking().getId()))
            self.bookRest(documentPosition, income, possession.getDefaultBooking())

    def getOrders(self, parentId):
        sql = "SELECT c FROM PossessionAutoPaymentOrder c JOIN c.possession ap WHERE ap.id = %s ORDER BY c.order ASC" % str(parentId)
        return entityManager.createQuery(sql).getResultList()

    def hasNegativeBalance(self, zpk):
        defaultPeriod = BookingPeriodManager().findDefaultBookingPeriod()
        balance = ZpkManager().findBalanceByZpkAndPeriod(zpk, defaultPeriod)
        return (balance.getCredit() - balance.getDebit()) < 0

    def book(self, documentPosition, income, zpk):
        defaultPeriod = BookingPeriodManager().findDefaultBookingPeriod()
        balance = ZpkManager().findBalanceByZpkAndPeriod(zpk, defaultPeriod)
        shouldBook = balance.getDebit() - balance.getCredit()
        if shouldBook > income:
            shouldBook = income
            income = 0
        else:
            income = income - shouldBook
        self.createAndBookPayment(documentPosition, shouldBook, zpk, defaultPeriod)
        return income
    
    def bookRest(self, documentPosition, income, zpk):
        defaultPeriod = BookingPeriodManager().findDefaultBookingPeriod()
        self.createAndBookPayment(documentPosition, income, zpk, defaultPeriod)

    def createAndBookPayment(self, position, income, zpk, period):
        vars.put('paymentDirection', 'INCOME')
        vars.put('paymentBook', 'true')
        vars.put('paymentAmount', float(income))
        vars.put('paymentType', self.getAutoPaymentType().getId())
        vars.put('accountId', self.getAccountId(position.getClientNumber()))
        vars.put('zpkId', zpk.getId())
        vars.put('paymentBookingPeriod', period.getId())
        vars.put('paymentDescription', position.getTitle())
        payment = PaymentManager().create()
        position.getPayments().add(payment)

    def getAutoPaymentType(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_TYPE', 'AUTO')

    def getAccountId(self, number):
        return AccountManager().findAccountByNumber(number).getId()
        
        
        