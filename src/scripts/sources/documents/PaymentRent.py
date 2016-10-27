from documents.Document import DocumentManager
from documents.validators.PaymentRentValidator import PaymentRentValidator
from java.math import BigDecimal
from java.math import RoundingMode
from structures.validators.common.ValidationError import ValidationError

class PaymentRentManager(DocumentManager):
    _type = "POSSESSION_PAYMENT"
    
    def create(self):
        try:
            payment = self.initDocument(self._type)
            account = self.findById('Account', self._svars.get('accountId'))
            self.handleOverpayment()
            if account != None and account.getType().getKey() in ['RENT', 'DEFAULT']:
                if self._svars.get('rentValue') != '' and float(self._svars.get('rentValue')) > 0:
                    self._svars.put('value', float(self._svars.get('rentValue')))
                if self._svars.get('value') != '' and float(self._svars.get('value')) != 0:
                    paymentPosition = self.initPosition(payment)
                    paymentPosition.setType("POSSESSION_PAYMENT_RENT")
                    paymentPosition.setDescription(self._svars.get('title'))
                    paymentPosition.setClientName(self._svars.get('sender'))
                    paymentPosition.putAttribute('CREATE_DATE', self._svars.get('creationDate'))
                    paymentPosition.putAttribute('BOOKING_DATE', self._svars.get('bookingDate'))
                    paymentPosition.setCreditZpk(self.findZpk(payment.getPossession().getZpks(), 'POSSESSION'))
                    paymentPosition.setDebitZpk(self.findZpk(paymentPosition.getAccount().getZpks(), 'RENT', 'DEFAULT'))
                    self.bound(payment, paymentPosition)
            if account != None and account.getType().getKey() in ['REPAIR_FUND', 'DEFAULT']:
                if self._svars.get('rfValue') != '' and float(self._svars.get('rfValue')) > 0:
                    self._svars.put('value', float(self._svars.get('rfValue')))
                if self._svars.get('value') != '' and float(self._svars.get('value')) != 0:
                    paymentPosition = self.initPosition(payment)
                    paymentPosition.setType("POSSESSION_PAYMENT_RF")
                    paymentPosition.setDescription(self._svars.get('title'))
                    paymentPosition.setClientName(self._svars.get('sender'))
                    paymentPosition.putAttribute('CREATE_DATE', self._svars.get('creationDate'))
                    paymentPosition.putAttribute('BOOKING_DATE', self._svars.get('bookingDate'))
                    paymentPosition.setCreditZpk(self.findZpk(payment.getPossession().getZpks(), 'POSSESSION_REPAIR_FUND'))
                    paymentPosition.setDebitZpk(self.findZpk(paymentPosition.getAccount().getZpks(), 'REPAIR_FUND'))
                    self.bound(payment, paymentPosition)
            PaymentRentValidator().validate(payment)
            self.saveDocument(payment)
        except ValidationError, error:
            self.setError(error)
    
    def remove(self):
        payment = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(payment)
        
    def handleOverpayment(self):
        if self._svars.get('overpayedValue') != '' and float(self._svars.get('overpayedValue')) > 0:
            howTo = self.findById("Dictionary", self._svars.get('overpayedId'))
            if howTo != None and howTo.getKey() == "RENT":
                value = BigDecimal(self._svars.get('rentValue')).add(BigDecimal(self._svars.get('overpayedValue'))).setScale(2, RoundingMode.HALF_UP)
                self._svars.put('rentValue', value.toString())
            elif howTo != None:
                value = BigDecimal(self._svars.get('rfValue')).add(BigDecimal(self._svars.get('overpayedValue'))).setScale(2, RoundingMode.HALF_UP)
                self._svars.put('rfValue', value.toString())
            else:
                raise ValidationError(self.findBy('Label', 'name', "'validators.document.payment.overpayment'").getMessage())
        
    def findZpk(self, zpks, typeKey, alternative=''):
        zpkType = self.findDictionary(str(self.findZpkSettingId(typeKey)))
        return [zpk for zpk in zpks if zpk.getType().getKey() == zpkType.getKey() or zpk.getType().getKey() == alternative][0]