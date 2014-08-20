from pl.reaper.container.data import Bank
from base.Container import Container
from entities.Company import CompanyManager

class BankManager(Container):
    
    def create(self):
        bank = Bank()
        self.setBankData(bank)
        self.saveBank(bank)
        
    def update(self):
        bank = self.findBank()
        self.setBankData(bank)
        self.saveBank(bank)
        
    def setBankData(self, bank):
        bank.setCompany(self.getCompany(bank))
        bank.setName(bank.getCompany().getName())
        bank.setKey(bank.getCompany().getName())
        
    def getCompany(self, bank):
        companyManager = CompanyManager()
        companyManager.setEntityManager(self._entityManager)
        companyManager.setSvars(self._svars)
        return companyManager.getCompany(bank)
        
    def saveBank(self, bank):
        self._logger.info(bank.longDescription())
        self._entityManager.persist(bank)
        self._entityManager.flush()

    def findBank(self):
        
        id = self._svars.get('id')
        return self.findBankById(id)

    def findBankById(self, id):
        return self._entityManager.createQuery('Select bank From Bank bank Where bank.id = ' + str(id)).getSingleResult()
    
    def findByLabel(self, label):
        return self._entityManager.createQuery("Select d From Bank d Join d.company c Where c.name = '%s'" % label).getSingleResult()
