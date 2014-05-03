from pl.reaper.container.data import Invoice
from entities.Contractor import ContractorManager
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
        if not invoice.isAccepted():
            self.addPositions()
        self.addPayments()
        self.saveInvoice(invoice)
        
    def setInvoiceData(self, invoice):
        self.setContractor(self.findContractor(self._svars.get('contractorId')))
        self.setCommunity(self.findCommunity(self._svars.get('communityId')))
        self.setCreateDate(self.parseDate(self._svars.get('createDate')))
        self.setPaymentDate(self.parseDate(self._svars.get('paymentDate')))
        self.setToPay(float(self._svars.get('toPay')))
        self.setPaymentsSum(float(self._svars.get('paymentsSum')))
        self.setAccepted(self.parseBoolean(self._svars.get('accepted'))

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
        pass

    def addPayments(self, payments):
        pass

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