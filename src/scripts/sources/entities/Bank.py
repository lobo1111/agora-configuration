from pl.reaper.container.data import Bank
from base.Container import Container
from entities.Company import CompanyManager

class BankManager(Container):
    
    def create(self):
        bank = Bank()
        self.setBankData(bank)
        self.saveEntity(bank)
        
    def update(self):
        bank = self.findById("Bank", self._svars.get('id'))
        self.setBankData(bank)
        self.saveEntity(bank)
        
    def setBankData(self, bank):
        bank.setCompany(CompanyManager().getCompany(bank))
        bank.setName(bank.getCompany().getName())
        bank.setKey(bank.getCompany().getName())
        
    def findByLabel(self, label):
        return self._entityManager.createQuery("Select d From Bank d Join d.company c Where c.name = '%s'" % label).getSingleResult()

    def getByAccountNumber(self, accountNumber):
        bankKey = accountNumber[2:6]
        bank = self.findBy('Bank', 'key', '"' + bankKey + '"')
        if bank == None:
            bank = Bank()
            bank.setCompany(CompanyManager().generateDummyCompany())
            bank.setName(bank.getCompany().getName())
            bank.setKey(bankKey)
            self.saveEntity(bank)
        return bank
