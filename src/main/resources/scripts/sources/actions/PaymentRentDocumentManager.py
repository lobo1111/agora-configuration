from actions.AbstractDocumentManager import AbstractDocumentManager

class PaymentRentDocumentManager(AbstractDocumentManager):
    
    def collectZpks(self, payment):
        possession = payment.getPossession()
        account = self.getAccount(payment)
        zpkCredit = self.findZpk(possession.getZpks(), 'POSSESSION')
        zpkDebit = self.findZpk(account.getZpks(), 'RENT', 'DEFAULT')
        return zpkCredit, zpkDebit
    
    def getAccount(self, payment):
        account = payment.getPaymentRentDetails().getAccount()
        if account.getType().getKey() == 'INDIVIDUAL':
            return account.getParrentAccount()
        else:
            return account
        
    def findZpk(self, zpks, typeKey, alternative = ''):
        zpkType = self.findZpkType(typeKey)
        self._logger.info('Looking for zpk type: %s' % zpkType.getKey())
        for zpk in zpks:
            self._logger.info('Checking: %s' % zpk.getType().getKey())
            if zpk.getType().getKey() == zpkType.getKey() or zpk.getType().getKey() == alternative:
                self._logger.info('Found it !')
                return zpk
    