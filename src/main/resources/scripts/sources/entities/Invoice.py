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
        self.saveInvoice(invoice)
        
    def update(self):
        invoice = self.findInvoice()
        self.calculateToPay(invoice)
        self.calculatePayed(invoice)
        if not invoice.isAccepted():
            self.addPositions(invoice)
        self.addPayments(invoice)
        self.saveInvoice(invoice)

    def removePosition(self):
        position = self.findInvoicePosition()
        if not position.getInvoice().isAccepted():
            position.getInvoice().getPositions().remove(position)
            self._entityManager.remove(position)
            self._entityManager.flush()
        self.calculateToPay(position.getInvoice())
        self._entityManager.persist(position.getInvoice())

    def removePayment(self):
        payment = self.findInvoicePayment()
        if not payment.isBooked():
            payment.getInvoice().getPayments().remove(payment)
            self._entityManager.remove(payment)
            self._entityManager.flush()
        self.calculatePayed(payment.getInvoice())
        self._entityManager.persist(payment.getInvoice())

    def calculateToPay(self, invoice):
        invoice.setToPay(sum([position.getValueGross() for position in invoice.getPositions()]))

    def calculatePayed(self, invoice):
        invoice.setPaymentsSum(sum([payment.getValuePayment() for payment in invoice.getPayments()]))
        
    def setInvoiceData(self, invoice):
        invoice.setContractor(self.findContractor(self._svars.get('contractorId')))
        invoice.setCommunity(self.findCommunity(self._svars.get('communityId')))
        invoice.setCreateDate(self.parseDate(self._svars.get('createDate')))
        invoice.setPaymentDate(self.parseDate(self._svars.get('paymentDate')))
        self.calculateToPay(invoice)
        self.calculatePayed(invoice)
        invoice.setAccepted(self.parseBoolean(self._svars.get('accepted')))

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
        for i in range(int(self._svars.get('positionsCount'))):
            positionId = self._svars.get(str(i) + '_positions_positionId')
            if positionId == '0':
                position = InvoicePosition()
                position.setName(self._svars.get(str(i) + '_positions_name'))
                position.setVolume(int(self._svars.get(str(i) + '_positions_volume')))
                position.setPosition(int(self._svars.get(str(i) + '_positions_position')))
                position.setValueNet(float(self._svars.get(str(i) + '_positions_netValue')))
                position.setValueGross(float(self._svars.get(str(i) + '_positions_grossValue')))
                position.setTax(self.findTax(self._svars.get(str(i) + '_positions_taxId')))
                position.setInvoice(invoice)
                invoice.getPositions().add(position)
                self._entityManager.persist(position)

    def addPayments(self, invoice):
        for i in range(int(self._svars.get('paymentsCount'))):
            paymentId = self._svars.get(str(i) + '_payments_paymentId')
            if paymentId == '0':
                payment = InvoicePayment()
                payment.setBooked(self.parseBoolean(self._svars.get(str(i) + '_payments_booked')))
                payment.setCreateDate(self.parseDate(self._svars.get(str(i) + '_payments_createDate')))
                payment.setValuePayment(float(self._svars.get(str(i) + '_payments_value')))
                payment.setInvoice(invoice)
                invoice.getPayments().add(payment)
                self._entityManager.persist(payment)

    def findTax(self, id):
        return DictionaryManager().getDictionaryInstance(int(id))

    def saveInvoice(self, invoice):
        self._entityManager.persist(invoice)
        self._entityManager.flush()
        
    def findInvoice(self):
        id = self._svars.get('id')
        return self.findInvoiceById(id)
        
    def findInvoicePosition(self):
        id = self._svars.get('positionId')
        return self.findInvoicePositionById(id)
        
    def findInvoicePayment(self):
        id = self._svars.get('paymentId')
        return self.findInvoicePaymentById(id)

    def findInvoiceById(self, id):
        try:
            return self._entityManager.createQuery('Select i From Invoice i Where i.id = ' + str(id)).getSingleResult()
        except:
            self._logger.error('Can\'t load invoice. Tried to load by id stored as ' + str(id))

    def findInvoicePositionById(self, id):
        try:
            return self._entityManager.createQuery('Select i From InvoicePosition i Where i.id = ' + str(id)).getSingleResult()
        except:
            self._logger.error('Can\'t load invoice position. Tried to load by id stored as ' + str(id))

    def findInvoicePaymentById(self, id):
        try:
            return self._entityManager.createQuery('Select i From InvoicePayment i Where i.id = ' + str(id)).getSingleResult()
        except:
            self._logger.error('Can\'t load invoice payment. Tried to load by id stored as ' + str(id))