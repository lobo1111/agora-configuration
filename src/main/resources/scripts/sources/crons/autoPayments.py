from pl.reaper.container.data import Payment

class CronAutoPayment(Container):
    _logger = Logger([:_scriptId])
    
    def processDocuments(self):
        self._logger.info('Cron auto payment started...')
        self._dictManager = DictionaryManager()
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
            self.createPaymentsFromDocument(document, possession)
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
        
    def createPaymentsFromDocument(self, document, possession):
        vars.put('income', document.getIncome().floatValue())
        vars.put('accountNumber', document.getClientNumber())
        vars.put('description', document.getTitle())
        payments = self.createPayments(possession)
        document.getPayments().addAll(payments)
    
    def createPayments(self, possession):
        income = vars.get('income')
        payments = []
        for order in self.getOrders(possession.getId()):
            zpk = order.getZpk()
            if income > 0 and self.hasNegativeBalance(zpk):
                (income, payment) = self.book(income, zpk)
                payments.append(payment)
        if income > 0:
            payment = self.bookRest(income, possession.getDefaultBooking())
            payment.append(payment)
        return payments

    def getOrders(self, parentId):
        sql = "SELECT c FROM PossessionAutoPaymentOrder c JOIN c.possession ap WHERE ap.id = %s ORDER BY c.order ASC" % str(parentId)
        return entityManager.createQuery(sql).getResultList()

    def hasNegativeBalance(self, zpk):
        defaultPeriod = BookingPeriodManager().findDefaultBookingPeriod()
        balance = ZpkManager().findBalanceByZpkAndPeriod(zpk, defaultPeriod)
        return (balance.getCredit() - balance.getDebit()) < 0

    def book(self, income, zpk):
        defaultPeriod = BookingPeriodManager().findDefaultBookingPeriod()
        balance = ZpkManager().findBalanceByZpkAndPeriod(zpk, defaultPeriod)
        shouldBook = balance.getDebit() - balance.getCredit()
        if shouldBook > income:
            shouldBook = income
            income = 0
        else:
            income = income - shouldBook
        self.createAndBookPayment(shouldBook, zpk, defaultPeriod)
        return (income, payment)
    
    def bookRest(self, income, zpk):
        defaultPeriod = BookingPeriodManager().findDefaultBookingPeriod()
        return self.createAndBookPayment(income, zpk, defaultPeriod)

    def createAndBookPayment(self, income, zpk, period):
        vars.put('paymentDirection', 'INCOME')
        vars.put('paymentBook', 'true')
        vars.put('paymentAmount', float(income))
        vars.put('paymentType', self.getAutoPaymentType().getId())
        vars.put('accountId', self.getAccountId(vars.get('accountNumber')))
        vars.put('zpkId', zpk.getId())
        vars.put('paymentBookingPeriod', period.getId())
        vars.put('paymentDescription', vars.get('description'))
        vars.put('paymentCommunityId', zpk.getCommunity().getId())
        payment = PaymentManager().create()
        position.getPayments().add(payment)
        return payment

    def getAutoPaymentType(self):
        return self._dictManager.findDictionaryInstance('PAYMENT_TYPE', 'AUTO')

    def getAccountId(self, number):
        return AccountManager().findAccountByNumber(number).getId()