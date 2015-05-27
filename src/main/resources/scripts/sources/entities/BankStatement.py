from base.Container import Container
from pl.reaper.container.data import InvoicePayment
from pl.reaper.container.data import PaymentRent
from java.text import SimpleDateFormat
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
        invoice = self.findById('Invoice', self._svars.get('invoiceId'))
        payment.setInvoice(invoice)
        payment.setValuePayment(float(self._svars.get('value')))
        payment.setCreateDate(self.parseDate(self._svars.get('createDate')))
        invoice.getPayments().add(payment)
        invoice.setPaymentsSum(sum([payment.getValuePayment() for payment in invoice.getPayments()]))
        self._entityManager.persist(payment)
        self._entityManager.persist(invoice)

    def createRentPayment(self):
        account = self.findById('Account', self._svars.get('accountId'))
        if account.getType().getKey() in ['RENT', 'DEFAULT']:
            paymentRent = self.createGenericPayment()
            if account.getType().getKey() in ['DEFAULT']:
                paymentRent.getPaymentRentDetails().setValue(float(self._svars.get('rent')))
            else:
                paymentRent.getPaymentRentDetails().setValue(float(self._svars.get('value')))
            paymentRent.setRepairFund(False)
            paymentRent.setComment(self._svars.get('comment'))
            self._entityManager.persist(paymentRent)
        if account.getType().getKey() in ['REPAIR_FUND', 'DEFAULT']:
            paymentRepairFund = self.createGenericPayment()
            if account.getType().getKey() in ['DEFAULT']:
                paymentRent.getPaymentRentDetails().setValue(float(self._svars.get('repairFund')))
            else:
                paymentRent.getPaymentRentDetails().setValue(float(self._svars.get('value')))
            paymentRepairFund.setRepairFund(True)
            paymentRepairFund.setComment(self._svars.get('comment'))
            self._entityManager.persist(paymentRepairFund)

    def createGenericPayment(self):
        payment = PaymentRent()
        payment.setPossession(self.findById('Possession', self._svars.get('possessionId')))
        payment.setBookingPeriod(self.findCurrentBookingPeriod())
        payment.setMonth(self.findCurrentMonth())
        payment.getPaymentRentDetails().setPaymentRent(payment)
        payment.getPaymentRentDetails().setRequestDate(self.parseDate(self._svars.get('requestDate')))
        payment.getPaymentRentDetails().setBookingDate(self.parseDate(self._svars.get('bookingDate')))
        payment.getPaymentRentDetails().setTitle(self._svars.get('title'))
        payment.getPaymentRentDetails().setClientName(self._svars.get('clientName'))
        payment.getPaymentRentDetails().setAccount(self.findById('Account', self._svars.get('accountId')))
        return payment

    def findCurrentBookingPeriod(self):
        return self._entityManager.createQuery('Select period From BookingPeriod period Where period.defaultPeriod = true').getSingleResult()

    def findCurrentMonth(self):
        return self._entityManager.createQuery('Select dict From Dictionary dict Join dict.type dtype Where dtype.type = "PERIODS" and dict.key = "CURRENT"').getSingleResult().getValue()

    