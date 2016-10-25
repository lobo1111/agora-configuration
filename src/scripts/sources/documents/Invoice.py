from documents.Document import DocumentManager
from documents.validators.InvoiceValidator import InvoiceValidator
from structures.validators.common.ValidationError import ValidationError
from pl.reaper.container.data import InvoicePositionDictionary
from java.math import BigDecimal
from java.math import RoundingMode

class InvoiceManager(DocumentManager):
    _type = "INVOICE"
    
    def persist(self):
        try:
            if self._svars.get("id") == '0':
                return self.create()
            else:
                return self.update()
        except ValidationError, error:
            self.setError(error)
        except IndexError, error:
            self.setError(InvoiceValidator().getNoZPKValidationError())
            
    def persistPayment(self):
        try:
            invoice = self.findById("Document", self._svars.get("invoiceId"))
            self.updatePayment(invoice)
            InvoiceValidator().validatePayments(invoice)
            self.saveDocument(invoice)
        except ValidationError, error:
            self.setError(error)
    
    def create(self):
        invoice = self.initDocument(self._type)
        self.updateInvoiceData(invoice)
        self.updatePositions(invoice)
        self.updatePayments(invoice)
        self.checkIfPayed(invoice)
        self.calculateValue(invoice)
        InvoiceValidator().validate(invoice)
        self.saveDocument(invoice)
        self.updatePositionsDictionary(invoice.getContractor().getCompany(), invoice.getPositions())
        return invoice
    
    def update(self):
        invoice = self.findById("Document", self._svars.get("id"))
        accepted = invoice.getAttribute("ACCEPTED").getValue()
        paymentOnly = self._svars.get("paymentOnly")
        if accepted == 'false' and (paymentOnly == None or (paymentOnly != None and paymentOnly != 'true')):
            self.updateInvoiceData(invoice)
            self.updatePositions(invoice)
        else:
            self._logger.info("Invoice already accepted, not updating details and positions")
        self.updatePayments(invoice)
        self.checkIfPayed(invoice)
        self.calculateValue(invoice)
        self.saveDocument(invoice)
        self.updatePositionsDictionary(invoice.getContractor().getCompany(), invoice.getPositions())
        return invoice
    
    def accept(self):
        invoice = self.findById("Document", self._svars.get("id"))
        invoice.putAttribute("ACCEPTED", 'true')
        self.saveDocument(invoice)
        
    def cancel(self):
        invoice = self.findById("Document", self._svars.get("id"))
        self.cancelDocument(invoice)
    
    def updateInvoiceData(self, invoice):
        invoice.putAttribute("NUMBER", self._svars.get('number'))
        invoice.putAttribute("PAYMENT_DATE", self._svars.get('paymentDate'))
        invoice.putAttribute("CREATE_DATE", self._svars.get('createDate'))
        invoice.putAttribute("ACCEPTED", 'false')
        invoice.putAttribute("PAYED", 'false')
        
    def calculateValue(self, invoice):
        value = BigDecimal(0.0)
        for position in invoice.getPositions():
            if position.getType() == "INVOICE_COST" and not position.isCanceled():
                value = value.add(position.getValue().setScale(2, RoundingMode.HALF_UP))
        invoice.putAttribute("VALUE", str(value.setScale(2, RoundingMode.HALF_UP).floatValue()))
        
    def checkIfPayed(self, invoice):
        costs = BigDecimal(0.0)
        payments = BigDecimal(0.0)
        for position in invoice.getPositions():
            if position.getType() == "INVOICE_COST" and not position.isCanceled():
                costs = costs.add(position.getValue())
            elif position.getType() == "INVOICE_PAYMENT" and not position.isCanceled():
                payments = payments.add(position.getValue())
        if costs.equals(payments):
            self._logger.info("Costs equals payments, marking as payed...")
            invoice.putAttribute("PAYED", 'true')
        else:
            self._logger.info("Costs(%f) doesn't equal payments(%f), marking as unpayed..." % (costs.floatValue(), payments.floatValue()))
            invoice.putAttribute("PAYED", 'false')
        
    def updatePositions(self, invoice):
        for i in range(int(self._svars.get('positions_size'))):
            if self._svars.get("positions_" + str(i) + "_" + 'id') != None:
                positionId = int(self._svars.get("positions_" + str(i) + "_" + 'id'))
            else:
                positionId = 0
            remove = self._svars.get("positions_" + str(i) + "_" + 'remove') == 'true'
            if remove and positionId != 0:
                position = self.findById("DocumentPosition", positionId)
                self.cancelPosition(position)
            elif not remove:
                position = self.findOrCreatePosition(invoice, positionId, 'positions_' + str(i))
                position.putAttribute("NUMBER", self._svars.get('positions_' + str(i) + "_" + 'number'))
                position.putAttribute("TAX_ID", self._svars.get('positions_' + str(i) + "_" + 'taxId'))
                position.putAttribute("VOLUME", self._svars.get('positions_' + str(i) + "_" + 'volume'))
                position.putAttribute("VALUE_UNIT", self._svars.get('positions_' + str(i) + "_" + 'unitValue'))
                position.putAttribute("VALUE_NET", self.calculateValueNet(position.getAttribute("VOLUME").getValue(), position.getAttribute("VALUE_UNIT").getValue()))
                position.setValue(self.calculateValueGross(position.getAttribute("VALUE_NET").getValue(), position.getAttribute("TAX_ID").getValue()))
                position.setDescription(self._svars.get('positions_' + str(i) + "_" + 'positionDescription'))
                if invoice.getContractor() != None:
                    position.setCreditZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR'))
                    position.setDebitZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR_COST'))
                self.bound(invoice, position)
    
    def updatePayments(self, invoice):
        for i in range(int(self._svars.get('payments_size'))):
            self.updatePayment(invoice, 'payments_' + str(i) + "_")
                
    def updatePayment(self, invoice, prefix = ''):
        self._logger.info("update Payment %s %s" % (invoice, prefix))
        if self._svars.get(prefix + 'id') != None and int(self._svars.get(prefix + 'id')) > 0:
            self._logger.info("BAM 1 !")
            paymentId = int(self._svars.get(prefix + 'id'))
        else:
            self._logger.info("BAM 2 !")
            paymentId = 0
        remove = self._svars.get(prefix + 'remove') == 'true'
        self._logger.info(remove)
        if remove and paymentId != 0:
            self._logger.info("BAM 3 !")
            payment = self.findById("DocumentPosition", paymentId)
            self.cancelPosition(payment)
        elif not remove and paymentId == 0:
            self._logger.info("BAM 4 !")
            payment = self.findOrCreatePayment(invoice, paymentId, prefix)
            payment.putAttribute("CREATE_DATE", self._svars.get(prefix + 'createDate'))
            payment.putAttribute("COST", self._svars.get(prefix + 'cost'))
            payment.putAttribute("COST_ID", self._svars.get(prefix + 'costId'))
            cost = self.findById("Dictionary", self._svars.get(prefix + 'costId'))
            if payment.getAccount() != None and invoice.getContractor() != None and cost != None:
                payment.setCreditZpk(self.findZpk(payment.getAccount().getZpks(), cost.getKey()))
                payment.setDebitZpk(self.findZpk(invoice.getContractor().getZpks(), 'CONTRACTOR'))
            self.bound(invoice, payment)
    
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
        
    def calculateValueNet(self, volume, unitPrice):
        try:
            bdVolume = BigDecimal(volume).setScale(2, RoundingMode.HALF_UP)
            bdUnitPrice = BigDecimal(unitPrice).setScale(2, RoundingMode.HALF_UP)
            return str(bdVolume.multiply(bdUnitPrice).setScale(2, RoundingMode.HALF_UP).floatValue())
        except:
            return '0'
    
    def calculateValueGross(self, valueNet, taxId):
        try:
            tax = self.findById("Dictionary", taxId)
            bdValueNet = BigDecimal(valueNet)
            bdTax = BigDecimal(tax.getKey())
            return bdValueNet.add(bdValueNet.multiply(bdTax).setScale(2, RoundingMode.HALF_UP)).setScale(2, RoundingMode.HALF_UP)
        except:
            return BigDecimal(0)
    
    def updatePositionsDictionary(self, company, positions):
        for position in positions:
            if position.getType() == "INVOICE_COST" and self.isNewPosition(company, position):
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
        