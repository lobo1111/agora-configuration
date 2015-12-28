from documents.Document import DocumentManager

class BankCreditManager(DocumentManager):
    _type = "BANK_CREDIT"
    
    def create(self):
        credit = self.initDocument(self._type)
        positionCost = self.initPosition(credit)
        positionCost.setType("BANK_CREDIT_COST")
        chargeDefaultAccount = self._svars.get("defaultAccount") == 'true'
        if chargeDefaultAccount:
            type = 'DEFAULT'
        else:
            type = 'REPAIR_FUND'
        credit.putAttribute("CHARGE_TYPE", type)
        credit.putAttribute("CREATE_DATE", self._svars.get('createdAt'))
        positionCost.setDebitZpk(self.findZpk(credit.getContractor().getZpks(), "CONTRACTOR_COST"))
        positionCost.setCreditZpk(self.findZpk(credit.getCommunity().getZpks(), type))
        self.bound(credit, positionCost)
        self.updatePayments(credit)
        return self.saveDocument(credit)
        
    def update(self):
        credit = self.findById("Document", self._svars.get('id'))
        self.updatePayments(credit)
        return self.saveDocument(credit)
        
    def cancel(self):
        credit = self.findById("Document", self._svars.get('id'))
        self.cancelDocument(credit)
        
    def markAsPayed(self):
        credit = self.findById("Document", self._svars.get('id'))
        self.closeDocument(credit)
        
    def updatePayments(self, credit):
        for i in range(int(self._svars.get('paymentsCount'))): 
            id = int(self._svars.get(str(i) + '_payments_' + 'paymentId'))
            remove = self._svars.get(str(i) + '_payments_' + 'remove') == 'true'
            if not remove:
                position = self.initPosition(credit, str(i) + '_payments_')
                position.setType("BANK_CREDIT_PAYMENT")
                position.putAttribute("CREATE_DATE", self._svars.get(str(i) + '_payments_' + 'createdAt'))
                position.setCreditZpk(self.findZpk(credit.getContractor().getZpks(), "CONTRACTOR"))
                position.setDebitZpk(self.findZpk(credit.getCommunity().getZpks(), credit.getAttribute('CHARGE_TYPE').getValue()))
                self.bound(credit, position)
            if id != 0 and remove:
                position = self.findById("DocumentPosition", id);
                self.cancelPosition(position)
                