from documents.Document import DocumentManager
from pl.reaper.container.data import InvoicePositionDictionary
from java.math import BigDecimal

class InvoiceManager(DocumentManager):
    _type = "INVOICE"
    
    def create(self):
        invoice = self.initDocument(self._type)
        self.updateInvoiceData(invoice)
        self.updatePositions(invoice)
        self.updatePayments(invoice)
        self.checkIfPayed(invoice)
        self.saveDocument(invoice)
        self.updatePositionsDictionary(invoice.getContractor().getCompany(), invoice.getPositions())
        return invoice
    
    def update(self):
        invoice = self.findById("Document", self.getParameter("id"))
        if not invoice.isAccepted():
            self.updateInvoiceData(invoice)
            self.updatePositions(invoice)
        self.updatePayments(invoice)
        self.checkIfPayed(invoice)
        self.saveDocument(invoice)
        self.updatePositionsDictionary(invoice.getContractor().getCompany(), invoice.getPositions())
        return invoice
    
    def accept(self):
        invoice = self.findById("Document", self.getParameter("id"))
        invoice.putAttribute("ACCEPTED", 'true')
        self.saveDocument(invoice)
    
    def updateInvoiceData(self, invoice):
        invoice.putAttribute("NUMBER", self.getParameter('number'))
        invoice.putAttribute("PAYMENT_DATE", self.getParameter('paymentDate'))
        invoice.putAttribute("CREATE_DATE", self.getParameter('createDate'))
        invoice.putAttribute("ACCEPTED", self.getParameter('accepted'))
        invoice.putAttribute("PAYED", 'false')
        
    def checkIfPayed(self, invoice):
        costs = BigDecimal(0.0)
        payments = BigDecimal(0.0)
        for position in invoice.getPositions():
            if position.getType() == "INVOICE_COST":
                costs = costs.add(BigDecimal(position.getAttribute("VALUE_GROSS").getValue()))
            elif position.getType() == "INVOICE_PAYMENT":
                payments = payments.add(position.getValue())
        if costs.equals(payments):
            invoice.putAttribute("PAYED", 'true')
        else:
            invoice.putAttribute("PAYED", 'false')
        
    def updatePositions(self, invoice):
        for i in range(int(self.getParameter('positionsCount'))):
            positionId = int(self.getParameter(str(i) + '_positions_positionId'))
            remove = self.getParameter(str(i) + '_positions_remove') == 'true'
            if remove and positionId != 0:
                position = self.findById("InvoiceItemPosition", positionId)
                self.cancelPosition(position)
            else:
                position = self.findOrCreatePosition(invoice, positionId, str(i) + '_positions_')
                position.putAttribute("NUMBER", self.getParameter(str(i) + '_positions_number'))
                position.putAttribute("TAX_ID", self.getParameter(str(i) + '_positions_taxId'))
                position.putAttribute("VOLUME", self.getParameter(str(i) + '_positions_volume'))
                position.putAttribute("VALUE_NET", self.getParameter(str(i) + '_positions_netValue'))
                position.putAttribute("VALUE_GROSS", self.getParameter(str(i) + '_positions_grossValue'))
                print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                print str(i) + '_positions_positionDescription'
                print self.getParameter(str(i) + '_positions_positionDescription')
                print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                position.setDescription(self.getParameter(str(i) + '_positions_positionDescription'))
                position.setCreditZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR'))
                position.setDebitZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR_COST'))
    
    def updatePayments(self, invoice):
        for i in range(int(self.getParameter('paymentsCount'))):
            self.updatePayment(invoice, str(i) + '_payments_')
                
    def updatePayment(self, invoice, prefix = ''):
        paymentId = int(self.getParameter(prefix + 'paymentId'))
        remove = self.getParameter(prefix + 'remove') == 'true'
        if remove and paymentId != 0:
            payment = self.findById("InvoicePaymentPosition", paymentId)
            self.cancelPosition(payment)
        else:
            payment = self.findOrCreatePayment(invoice, paymentId, prefix)
            payment.setCreditZpk(self.findZpk(invoice.getCommunity().getZpks(), 'RENT'))
            payment.setDebitZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR'))
    
    def findOrCreatePosition(self, invoice, positionId, prefix):
        if positionId == 0:
            position = self.initPosition(invoice, prefix)
            position.setType("INVOICE_COST")
            return position
        else:
            return self.findById("DocumentPosition", positionId)
    
    def findOrCreatePayment(self, invoice, paymentId, prefix):
        if paymentId == 0:
            position = self.initPosition(invoice, prefix)
            position.setType("INVOICE_PAYMENT")
            return position
        else:
            return self.findById("DocumentPosition", paymentId)
    
    def updatePositionsDictionary(self, company, positions):
        for position in positions:
            if self.isNewPosition(company, position):
                self.storePosition(company, position)
                
    def isNewPosition(self, company, position):
        count = self._entityManager.createQuery("Select count(p) From InvoicePositionDictionary p Where p.company.id = %d and p.position = '%s'" % (company.getId(), position.getDescription())).getSingleResult()
        return count == 0
        
    def storePosition(self, company, position):
        d = InvoicePositionDictionary();
        d.setCompany(company)
        d.setPosition(position.getDescription())
        self._logger.info('Registering new position on invoice dictionary: %s' % d.getPosition())
        self.saveEntity(d, putId = False)
        