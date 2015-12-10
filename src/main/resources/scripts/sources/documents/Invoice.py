from document.Document import Document
from pl.reaper.container.data import Invoice
from pl.reaper.container.data import InvoiceItemPosition
from pl.reaper.container.data import InvoicePaymentPosition

class Invoice(Document):
    
    def create(self):
        invoice = self.initDocument(Invoice(), Invoice.TYPE)
        self.updateInvoiceData(invoice)
        self.updatePositions(invoice)
        self.updatePayments(invoice)
        self.updatePositionsDictionary(invoice.getContractor().getCompany(), invoice.getPositions())
        return self.saveDocument(invoice)
    
    def update(self):
        invoice = self.findById("Invoice", self._svars.get("id"))
        if not invoice.isAccepted():
            self.updateInvoiceData(invoice)
            self.updatePositions(invoice)
        self.updatePayments(invoice)
        self.updatePositionsDictionary(invoice.getContractor().getCompany(), invoice.getPositions())
        return self.saveDocument(invoice)
    
    def updateInvoiceData(self, invoice):
        invoice.setNumber(self._svars.get('number'))
        invoice.setContractor(self.findContractor(self._svars.get('contractorId')))
        invoice.setPaymentDate(self.parseDate(self._svars.get('paymentDate')))
        invoice.setCreateDate(self.parseDate(self._svars.get('createDate')))
        
    def updatePositions(self, invoice):
        for i in range(int(self._svars.get('positionsCount'))):
            positionId = int(self._svars.get(str(i) + '_positions_positionId'))
            remove = self._svars.get(str(i) + '_positions_remove') == 'true'
            if remove and positionId != 0:
                position = self.findById("InvoiceItemPosition", positionId)
                self.cancelPosition(position)
            else:
                position = self.findOrCreatePosition(invoice, positionId)
                position.setDescription(self._svars.get(str(i) + '_positions_name'))
                position.setVolume(float(self._svars.get(str(i) + '_positions_volume')))
                position.setNumber(int(self._svars.get(str(i) + '_positions_number')))
                position.setUnitValueNet(float(self._svars.get(str(i) + '_positions_unitValueNet')))
                position.setValueNet(float(self._svars.get(str(i) + '_positions_netValue')))
                position.setValueGross(float(self._svars.get(str(i) + '_positions_grossValue')))
                position.setTax(self.findTax(self._svars.get(str(i) + '_positions_taxId')))
                position.setCreditZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR'))
                position.setDebitZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR_COST'))
    
    def updatePayments(self, invoice):
        for i in range(int(self._svars.get('paymentsCount'))):
            paymentId = self._svars.get(str(i) + '_payments_paymentId')
            remove = self._svars.get(str(i) + '_payments_remove') == 'true'
            if remove and paymentId != 0:
                payment = self.findById("InvoicePaymentPosition", paymentId)
                self.cancelPosition(payment)
            else:
                payment = self.findOrCreatePayment(invoice, paymentId)
                payment.setCreditZpk(self.findZpk(invoice.getCommunity().getZpks(), 'RENT'))
                payment.setDebitZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR'))
    
    def findOrCreatePosition(self, invoice, positionId):
        if positionId == 0:
            return self.initPosition(invoice, InvoiceItemPosition(), '_positions_')
        else:
            return self.findById("InvoiceItemPosition", positionId)
    
    def findOrCreatePayment(self, invoice, paymentId):
        if paymentId == 0:
            return self.initPosition(invoice, InvoicePaymentPosition(), '_payments_')
        else:
            return self.findById("InvoicePaymentPosition", paymentId)
    
    def updatePositionsDictionary(self, company, positions):
        for position in positions:
            if self.isNewPosition(company, position):
                self.storePosition(company, position)
                
    def isNewPosition(self, company, position):
        count = self._entityManager.createQuery("Select count(p) From InvoicePositionDictionary p Where p.company.id = %d and p.position = '%s'" % (company.getId(), position.getName())).getSingleResult()
        return count == 0
        
    def storePosition(self, company, position):
        d = InvoicePositionDictionary();
        d.setCompany(company)
        d.setPosition(position.getName())
        self._entityManager.persist(d)
        