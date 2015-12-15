from documents.Document import DocumentManager

class InvoiceManager(DocumentManager):
    _type = "INVOICE"
    
    def create(self):
        invoice = self.initDocument(self._type)
        self.updateInvoiceData(invoice)
        self.updatePositions(invoice)
        self.updatePayments(invoice)
        self.updatePositionsDictionary(invoice.getContractor().getCompany(), invoice.getPositions())
        return self.saveDocument(invoice)
    
    def update(self):
        invoice = self.findById("Document", self._svars.get("id"))
        if not invoice.isAccepted():
            self.updateInvoiceData(invoice)
            self.updatePositions(invoice)
        self.updatePayments(invoice)
        self.updatePositionsDictionary(invoice.getContractor().getCompany(), invoice.getPositions())
        return self.saveDocument(invoice)
    
    def accept(self):
        invoice = self.findById("Document", self._svars.get("id"))
        invoice.setAccepted(True)
        self.saveDocument(invoice)
    
    def updateInvoiceData(self, invoice):
        invoice.addAttribute("NUMBER", self._svars.get('number'))
        invoice.addAttribute("PAYMENT_DATE", self._svars.get('paymentDate'))
        invoice.addAttribute("CREATE_DATE", self._svars.get('createDate'))
        invoice.addAttribute("ACCEPTED", self._svars.get('accepted') == True)
        
    def updatePositions(self, invoice):
        for i in range(int(self._svars.get('positionsCount'))):
            positionId = int(self._svars.get(str(i) + '_positions_positionId'))
            remove = self._svars.get(str(i) + '_positions_remove') == 'true'
            if remove and positionId != 0:
                position = self.findById("InvoiceItemPosition", positionId)
                self.cancelPosition(position)
            else:
                position = self.findOrCreatePosition(invoice, positionId)
                position.addAttribute("NUMBER", self._svars.get(str(i) + '_positions_number'))
                position.addAttribute("TAX_ID", self._svars.get(str(i) + '_positions_taxId'))
                position.addAttribute("VOLUME", float(self._svars.get(str(i) + '_positions_volume')))
                position.addAttribute("VALUE_NET", float(self._svars.get(str(i) + '_positions_netValue')))
                position.addAttribute("VALUE_GROSS", float(self._svars.get(str(i) + '_positions_grossValue')))
                position.setDescription(self._svars.get(str(i) + '_positions_name'))
                position.setValue(float(self._svars.get(str(i) + '_positions_unitValueNet')))
                position.setCreditZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR'))
                position.setDebitZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR_COST'))
    
    def updatePayments(self, invoice):
        for i in range(int(self._svars.get('paymentsCount'))):
            self.updatePayment(invoice, str(i), '_payments_')
                
    def updatePayment(self, invoice, counter = '', prefix = ''):
        paymentId = int(self._svars.get(counter + prefix + 'paymentId'))
        remove = self._svars.get(counter + prefix + 'remove') == 'true'
        if remove and paymentId != 0:
            payment = self.findById("InvoicePaymentPosition", paymentId)
            self.cancelPosition(payment)
        else:
            payment = self.findOrCreatePayment(invoice, paymentId, prefix)
            payment.setCreditZpk(self.findZpk(invoice.getCommunity().getZpks(), 'RENT'))
            payment.setDebitZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR'))
    
    def findOrCreatePosition(self, invoice, positionId):
        if positionId == 0:
            position = self.initPosition(invoice, '_positions_')
            posiiton.setType("INVOICE_COST")
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
        count = self._entityManager.createQuery("Select count(p) From InvoicePositionDictionary p Where p.company.id = %d and p.position = '%s'" % (company.getId(), position.getName())).getSingleResult()
        return count == 0
        
    def storePosition(self, company, position):
        d = InvoicePositionDictionary();
        d.setCompany(company)
        d.setPosition(position.getName())
        self._entityManager.persist(d)
        