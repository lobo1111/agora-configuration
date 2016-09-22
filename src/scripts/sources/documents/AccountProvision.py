from documents.Document import DocumentManager
from documents.validators.AccountProvisionValidator import AccountProvisionValidator
from structures.validators.common.ValidationError import ValidationError

class AccountProvisionManager(DocumentManager):
    _type = "ACCOUNT_PROVISION"
    
    def persist(self):
        try:
            return self.create()
        except ValidationError, error:
            self.setError(error)
    
    def create(self):
        provision = self.initDocument(self._type)
        position = self.initPosition(provision)
        position.setCreditZpk(self.findZpk(provision.getCommunity().getZpks(), 'RENT'))
        if position.getAccount() != None:
            position.setDebitZpk(self.findZpk(position.getAccount().getBankContractor().getZpks(), 'CONTRACTOR'))
        self.bound(provision, position)
        AccountProvisionValidator().validate(provision)
        return self.saveDocument(provision)
    
    def cancel(self):
        provision = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(provision)