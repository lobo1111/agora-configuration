from documents.Document import DocumentManager

class BankCreditManager(DocumentManager):
    _type = "BANK_CREDIT"
    
    def create(self):
        credit = self.initDocument(self._type)
        positionCost = self.initPosition(credit)
        positionCost.setType("BANK_CREDIT_COST")
        positionCost.setZpkCredit(self.findZpk(credit.getContractor().getZpks(), 'CONTRACTOR'))
        chargeDefaultAccount = self._svars.get("defaultAccount") == 'true'
        if chargeDefaultAccount:
            type = 'RENT'
        else:
            type = 'REPAIR_FUND'
        credit.putAttribute("CHARGE_TYPE", type)
        positionCost.setZpkDebit(self.findZpk(credit.getContractor().getZpks(), "CONTRACTOR_COST"))
        positionCost.setZpkCredit(self.findZpk(credit.getCommunity().getZpks(), type))
        self.bound(credit, positionCost)
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
                position = self.initPosition(credit, '_payments_')
                position.setType("BANK_CREDIT_PAYMENT")
                position.setZpkCredit(self.findZpk(credit.getContractor().getZpks(), "CONTRACTOR"))
                position.setZpkDebit(self.findZpk(credit.getCommunity().getZpks(), credit.getAttribute('CHARGE_TYPE')))
                self.bound(credit, position)
            if id != 0 and remove:
                position = self.findById("DocumentPosition", id);
                self.cancelPosition(position)
                