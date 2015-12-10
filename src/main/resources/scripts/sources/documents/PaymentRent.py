from document.Document import Document
from pl.reaper.container.data import PossessionPayment
from pl.reaper.container.data import PossessionPaymentPosition

class PaymentRent(Document):
    
     def create(self):
        payment = self.initDocument(PossessionPayment(), PaymentRent.TYPE)
        payment.setPossession(self.findById("Possession", self._svars.get("possessionId")))
        payment.setRepairFund(isRepairFund)
        paymentPosition = self.initPosition(payment, PossessionPaymentPosition())
        paymentPosition.setClientName(self._svars.get('clientName'))
        paymentPosition.setAccount(self.findById("Account", self._svars.get("accountId")))
        isRepairFund = self._svars.get('repairFund') == 'true'
        if isRepairFund():
            paymentPosition.setCreditZpk(self.findZpk(payment.getPossession().getZpks(), 'POSSESSION_REPAIR_FUND'))
            paymentPosition.setDebitZpk(self.findZpk(paymentPosition.getAccount().getZpks(), 'REPAIR_FUND'))
        else:
            paymentPosition.setCreditZpk(self.findZpk(payment.getPossession().getZpks(), 'POSSESSION'))
            paymentPosition.setDebitZpk(self.findZpk(paymentPosition.getAccount().getZpks(), 'RENT', 'DEFAULT'))
        self.saveDocument(payment)
        
    def remove(self):
        payment = self.findById("PossessionPayment", self._svars.get('id'))
        self.cancelDocument(payment)
        
    def findZpk(self, zpks, typeKey, alternative = ''):
        zpkType = self.findZpkType(typeKey)
        for zpk in zpks:
            if zpk.getType().getKey() == zpkType.getKey() or zpk.getType().getKey() == alternative:
                return zpk