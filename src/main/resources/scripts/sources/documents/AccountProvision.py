from documents.Document import DocumentManager

class AccountProvisionManager(DocumentManager):
    _type = "ACCOUNT_PROVISION"
    
    def create(self):
        provision = self.initDocument(self._type)
        position = self.initPosition(provision)
        position.setAccount(self.findById("Account", self._svars.get('accountId')))
        position.setZpkCredit(self.findZpk(provision.getCommunity().getZpks(), 'RENT'))
        position.setZpkDebit(self.findZpk(provision.getAccount().getBankContractor().getZpks(), 'CONTRACTOR'))
        return self.saveDocument(provision)
    
    def remove(self):
        provision = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(provision)