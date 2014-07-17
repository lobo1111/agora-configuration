from base.Container import Container
from pl.reaper.container.data import InvoicePayment
from pl.reaper.container.data import PaymentRent
import sys

class BankStatementManager(Container):
    
    def create(self):
        invoiceType = self._svars.get('invoiceType')
        if invoiceType == 'true':
            self.createInvoicePayment()
        else:
            self.createRentPayment()

    def createInvoicePayment(self):
        payment = InvoicePayment()
        payment.setInvoice(self.findInvoiceById(self._svars.get('invoiceId')))
        payment.setValuePayment(float(self._svars.get('value')))
        payment.setCreateDate(self.parseDate(self._svars.get('createDate')))
        #self._entityManager.persist(payment)

    def createRentPayment(self):
        payment = PaymentRent()
        payment.setPossession(self.findPossessionById(self._svars.get('possessionId')))
        payment.setBookingPeriod(self.findCurrentBookingPeriod())
        payment.setMonth(self.findCurrentMonth())
        payment.getPaymentRentDetails().setPaymentRent(payment)
        payment.getPaymentRentDetails().setValue(float(self._svars.get('value')))
        payment.getPaymentRentDetails().setRequestDate(self.parseDate(self._svars.get('requestDate')))
        payment.getPaymentRentDetails().setBookingDate(self.parseDate(self._svars.get('bookingDate')))
        payment.getPaymentRentDetails().setTitle(self._svars.get('title'))
        payment.getPaymentRentDetails().setClientName(self._svars.get('clientName'))
        payment.getPaymentRentDetails().setAccount(self.findAccountById(self._svars.get('accountId')))
        self._entityManager.persist(payment)

    def findCurrentBookingPeriod(self):
        return self._entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()

    def findCurrentMonth(self):
        return self._entityManager.createQuery('Select dict From Dictionary dict Join dict.type dtype Where dtype.type = "PERIODS" and dict.key = "CURRENT"').getSingleResult().getValue()

    def findInvoiceById(self, id):
        return self._entityManager.createQuery('Select i From Invoice i Where i.id = ' + str(id)).getSingleResult()
        
    def findPossessionById(self, id):
        return self._entityManager.createQuery('Select i From Possession i Where i.id = ' + str(id)).getSingleResult()
        
    def findAccountById(self, id):
        return self._entityManager.createQuery('Select i From Account i Where i.id = ' + str(id)).getSingleResult()

    def parseDate(self, dateAsString):
        try:
            self._logger.info('Parsing date from str(%s) into %s' % (dateAsString, SimpleDateFormat('dd-MM-yyyy').parse(dateAsString)))
            return SimpleDateFormat('dd-MM-yyyy').parse(dateAsString)
        except:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            self._logger.info('Cant parse !')
            self._logger.info(exc_value)
            return None
    