from documents.Document import DocumentManager

class BankCreditManager(DocumentManager):
    _type = "BANK_CREDIT"
    
    def create(self):
        credit = self.initDocument(self._type)
        credit.setContractor(self.findById("Contractor", self._svars.get("contractorId")))
        positionCost = self.initPosition(credit)
        positionCost.setZpkCredit(self.findZpk(credit.getContractor().getZpks(), 'CONTRACTOR'))
        chargeDefaultAccount = self._svars.get("defaultAccount") == 'true'
        if chargeDefaultAccount:
            type = 'RENT'
        else:
            type = 'REPAIR_FUND'
        positionCost.setZpkDebit(self.findZpk(credit.getCommunity().getZpks(), type))
        self.updatePayments(credit)
        return self.saveDocument(credit)
        
    def update(self):
        credit = self.findById("Document", self._svars.get('id'))
        self.updatePayments(credit)
        return self.saveDocument(credit)
        
    def remove(self):
        credit = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(credit)
        
    def markAsPayed(self):
        credit = self.findById("Document", self._svars.get('id'))
        self.closeDocument(credit)
        
    def updatePayments(self, credit):
        for i in range(int(self._svars.get('paymentsCount'))): 
            id = int(self._svars.get(str(i) + '_payments_' + 'paymentId'))
            remove = self._svars.get(str(i) + '_payments_' + 'remove') == 'true'
            if id == 0 and not remove:
                self.initPosition(credit, '_payments_')
            if id != 0 and remove:
                position = self.findById("DocumentPosition", id);
                self.cancelPosition(position)
                