from documents.Document import DocumentManager

class AccountProvisionManager(DocumentManager):
    _type = "ACCOUNT_PROVISION"
    
    def create(self):
        provision = self.initDocument(self._type)
        position = self.initPosition(provision)
        position.setZpkCredit(self.findZpk(provision.getCommunity().getZpks(), 'RENT'))
        position.setZpkDebit(self.findZpk(provision.getAccount().getBankContractor().getZpks(), 'CONTRACTOR'))
        self.bound(provision, position)
        return self.saveDocument(provision)
    
    def cancel(self):
        provision = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(provision)