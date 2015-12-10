from documents.Document import Document
from pl.reaper.container.data import AccountProvision
from pl.reaper.container.data import AccountProvisionPosition

class AccountProvision(Document):
    
    def create(self):
        provision = self.initDocument(AccountProvision(), AccountProvision.TYPE)
        position = self.initPosition(provision, AccountProvisionPosition())
        position.setAccount(self.findById("Account", self._svars.get('accountId')))
        position.setZpkCredit(self.findZpk(provision.getCommunity().getZpks(), 'RENT'))
        position.setZpkDebit(self.findZpk(provision.getAccount().getBankContractor().getZpks(), 'CONTRACTOR'))
        return self.saveDocument(provision)
    
    def remove(self):
        provision = self.findById("AccountProvision", self._svars.get('id'))
        self.cancelDocument(provision)