from base.Container import Container
from entities.InternalPayment import InternalPaymentManager

class InvoiceBookerManager(Container):
    
    def bookAllInvoices(self):
        self._logger.info("Invoice Booker starts...")
        [self.bookInvoice(invoice) for invoice in self.collectInvoices()]
        self._logger.info("All invoices booked")
        
    def collectInvoices(self):
        sql = 'Select i From Invoice i Left Outer Join i.payments ps Where i.booked = false or ps.booked = false'
        return self._entityManager.createQuery(sql).getResultList()
    
    def bookInvoice(self, invoice):
        self._logger.info("Booking invoice %d" % invoice.getId())
        if not invoice.isBooked():
            self.bookCost(invoice)
        [self.bookPayment(payment) for payment in invoice.getPayments() if not payment.isBooked()]

    def bookCost(self, invoice):
        creditZpk = self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR')
        debitZpk = self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR_COST')
        self.createAndBookPayment(creditZpk, debitZpk, invoice.getToPay())
        invoice.setBooked(True)
        self._entityManager.persist(invoice)

    def bookPayment(self, payment):
        creditZpk = self.findZpk(payment.getInvoice().getCommunity().getZpks(), 'RENT')
        debitZpk = self.findZpk(payment.getInvoice().getContractor().getZpks(), 'CONTRACTOR')
        self.createAndBookPayment(creditZpk, debitZpk, payment.getValuePayment())
        payment.setBooked(True)
        self._entityManager.persist(payment)
                
    def createAndBookPayment(self, creditZpk, debitZpk, amount):
        self._svars.put('creditZpkId', str(creditZpk.getId()))
        self._svars.put('debitZpkId', str(debitZpk.getId()))
        self._svars.put('amount', str(amount))
        self._svars.put('comment', 'Faktura')
        manager = InternalPaymentManager()
        manager.setEntityManager(self._entityManager)
        manager.setSvars(self._svars)
        payment = manager.create()
        self._entityManager.flush()
        self._svars.put('paymentId', str(payment.getId()))
        manager.book()
        
    def findZpk(self, zpks, typeKey):
        zpkType = self.findZpkType(typeKey)
        return [zpk for zpk in zpks if zpk.getType().getKey() == zpkType.getKey()][0]
            
    def findZpkType(self, typeKey):
        return self.findDictionary(str(self.findZpkSettingId(typeKey)))
    
    def findDictionary(self, id):
        return self._entityManager.createQuery("Select d From	Dictionary d Where d.id = %s" % str(id)).getSingleResult()
    
    def findZpkSettingId(self, typeKey):
        return self._entityManager.createQuery("Select ds.value From Dictionary ds join ds.type ts Where ts.type = 'ZPKS_SETTINGS' and ds.key = '%s'" % typeKey).getSingleResult()