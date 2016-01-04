from documents.Document import DocumentManager

class PaymentRentManager(DocumentManager):
    _type = "POSSESSION_PAYMENT"
    
    def create(self):
        payment = self.initDocument(self._type)
        account = payment.getAccount()
        if account.getType().getKey() in ['RENT', 'DEFAULT']:
            if account.getType().getKey() == 'RENT':
                value = float(self._svars.get('rent'))
            else:
                value = float(self._svars.get('value'))
            if value != 0:
                paymentPosition = self.initPosition(payment)
                paymentPosition.setClientName(self._svars.get('clientName'))
                paymentPosition.setAccount(account)
                paymentPosition.setCreditZpk(self.findZpk(payment.getPossession().getZpks(), 'POSSESSION'))
                paymentPosition.setDebitZpk(self.findZpk(paymentPosition.getAccount().getZpks(), 'RENT', 'DEFAULT'))
        if account.getType().getKey() in ['REPAIR_FUND', 'DEFAULT']:
            if account.getType().getKey() == 'REPAIR_FUND':
                value = float(self._svars.get('repairFund'))
            else:
                value = float(self._svars.get('value'))
            if value != 0:
                paymentPosition = self.initPosition(payment)
                paymentPosition.setClientName(self._svars.get('clientName'))
                paymentPosition.setAccount(account)
                paymentPosition.setCreditZpk(self.findZpk(payment.getPossession().getZpks(), 'POSSESSION_REPAIR_FUND'))
                paymentPosition.setDebitZpk(self.findZpk(paymentPosition.getAccount().getZpks(), 'REPAIR_FUND'))
        self.saveDocument(payment)
    
    def remove(self):
        payment = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(payment)
        
    def findZpk(self, zpks, typeKey, alternative = ''):
        zpkType = self.findZpkType(typeKey)
        for zpk in zpks:
            if zpk.getType().getKey() == zpkType.getKey() or zpk.getType().getKey() == alternative:
                return zpk