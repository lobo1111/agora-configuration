from pl.reaper.container.data import Invoice
from pl.reaper.container.data import InvoicePosition
from pl.reaper.container.data import InvoicePayment
from entities.Contractor import ContractorManager
from entities.Dictionary import DictionaryManager
from entities.Community import CommunityManager
from java.text import SimpleDateFormat
from base.Container import Container

class InvoiceManager(Container):
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix
        
    def create(self):
        invoice = Invoice()
        self.setInvoiceData(invoice)
        self.addPositions(invoice)
        self.addPayments(invoice)
        self.calculateToPay(invoice)
        self.calculatePayed(invoice)
        self.saveInvoice(invoice)
        
    def update(self):
        self._logger.info("Update")
        invoice = self.findInvoice()
        if not invoice.isAccepted():
            invoice.setNumber(self._svars.get('number'))
            self.addPositions(invoice)
        self._logger.info("before")
        self.addPayments(invoice)
        self._logger.info("after")
        self.calculateToPay(invoice)
        self.calculatePayed(invoice)
        self.saveInvoice(invoice)

    def accept(self):
        invoice = self.findInvoice()
        if not invoice.isAccepted():
            invoice.setAccepted(True)
            self._logger.info("Invoice accepted(%d)" % invoice.getId())
            self.saveInvoice(invoice)

    def cancel(self):
        invoice = self.findInvoice()
        if len([invoicePayment for invoicePayment in invoice.getPayments() if invoicePayment.isBooked()]) == 0:
            self._logger.info("Canceling invoice(%d)..." % invoice.getId())
            [self._entityManager.remove(invoicePayment) for invoicePayment in invoice.getPayments()]
            [self._entityManager.remove(invoicePosition) for invoicePosition in invoice.getPositions()]
            self._entityManager.remove(invoice)
        else:
            self._logger.info("Invoice(%d) contains booked payments, can't be canceled" % invoice.getId())

    def calculateToPay(self, invoice):
        invoice.setToPay(sum([position.getValueGross() for position in invoice.getPositions()]))

    def calculatePayed(self, invoice):
        invoice.setPaymentsSum(sum([payment.getValuePayment() for payment in invoice.getPayments()]))
        
    def setInvoiceData(self, invoice):
        invoice.setContractor(self.findContractor(self._svars.get('contractorId')))
        invoice.setCommunity(self.findCommunity(self._svars.get('communityId')))
        invoice.setCreateDate(self.parseDate(self._svars.get('createDate')))
        invoice.setPaymentDate(self.parseDate(self._svars.get('paymentDate')))
        invoice.setAccepted(self.parseBoolean(self._svars.get('accepted')))
        invoice.setNumber(self._svars.get('number'))

    def findContractor(self, id):
        return ContractorManager().findContractorById(id)

    def findCommunity(self, id):
        return CommunityManager().findCommunityById(id)

    def parseDate(self, dateAsString):
        try:
            return SimpleDateFormat('dd-MM-yy').parse(dateAsString)
        except:
            return None

    def parseBoolean(self, boolean):
        return boolean == 'true'

    def addPositions(self, invoice):
        notToRemove = []
        toRemove = []
        for i in range(int(self._svars.get('positionsCount'))):
            positionId = self._svars.get(str(i) + '_positions_positionId')
            if positionId == '0':
                position = InvoicePosition()
            else:
                position = self.findPositionById(positionId)
            position.setName(self._svars.get(str(i) + '_positions_name'))
            position.setVolume(int(self._svars.get(str(i) + '_positions_volume')))
            position.setPosition(int(self._svars.get(str(i) + '_positions_position')))
            position.setValueNet(float(self._svars.get(str(i) + '_positions_netValue')))
            position.setValueGross(float(self._svars.get(str(i) + '_positions_grossValue')))
            position.setTax(self.findTax(self._svars.get(str(i) + '_positions_taxId')))
            position.setInvoice(invoice)
            invoice.getPositions().add(position)
            self._entityManager.persist(position)
            self._entityManager.flush()
            notToRemove.append(position.getId())
        for position in invoice.getPositions():
            if not (position.getId() in notToRemove):
                toRemove.append(position)
        for position in toRemove:
            invoice.getPositions().remove(position)


    def addPayments(self, invoice):
        notToRemove = []
        toRemove = []
        self._logger.info('registered payments: ' + str(invoice.getPayments().size()))
        for i in range(int(self._svars.get('paymentsCount'))):
            paymentId = self._svars.get(str(i) + '_payments_paymentId')
            if paymentId == '0':
                payment = InvoicePayment()
            else:
                payment = self.findPaymentById(paymentId)
            payment.setBooked(self.parseBoolean(self._svars.get(str(i) + '_payments_booked')))
            payment.setCreateDate(self.parseDate(self._svars.get(str(i) + '_payments_createDate')))
            payment.setValuePayment(float(self._svars.get(str(i) + '_payments_value')))
            payment.setInvoice(invoice)
            invoice.getPayments().add(payment)
            self._entityManager.persist(payment)
            self._entityManager.flush()
            notToRemove.append(payment.getId())
            self._logger.info('payment not to remove: ' + str(payment.getId()))
            
        for payment in invoice.getPayments():
            if not (payment.getId() in notToRemove):
                toRemove.append(payment)
                self._logger.info('payment to remove: ' + str(payment.getId()))
            else:
                self._logger.info('payment will be spared: ' + str(payment.getId()))
        for payment in toRemove:
            self._logger.info('payment removed: ' + str(payment.getId()))
            invoice.getPayments().remove(payment)

    def findTax(self, id):
        return DictionaryManager().getDictionaryInstance(int(id))

    def saveInvoice(self, invoice):
        self._entityManager.persist(invoice)
        self._entityManager.flush()
        
    def findInvoice(self):
        id = self._svars.get('id')
        return self.findInvoiceById(id)
        
    def findInvoiceById(self, id):
        try:
            return self._entityManager.createQuery('Select i From Invoice i Where i.id = ' + str(id)).getSingleResult()
        except:
            self._logger.error('Can\'t load invoice. Tried to load by id stored as ' + str(id))

    def findPositionById(self, id):
        return self._entityManager.createQuery('Select i From InvoicePosition i Where i.id = ' + str(id)).getSingleResult()

    def findPaymentById(self, id):
        return self._entityManager.createQuery('Select i From InvoicePayment i Where i.id = ' + str(id)).getSingleResult()