from pl.reaper.container.data import Bank

class BankManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        bank = Bank()
        self.setBankData(bank)
        self.saveBank(bank)
        
    def update(self):
        bank = self.findBank()
        self.setBankData(bank)
        self.saveBank(bank)
        
    def setBankData(self, bank):
        bank.setName(vars.get('bankName'))
        bank.setKey(vars.get('bankKey'))
        bank.setCompany(self.getCompany(bank))
        
    def getCompany(self, bank):
        companyManager = CompanyManager()
        return companyManager.getCompany(bank)
        
    def saveBank(self, bank):
        self._logger.info(bank.longDescription())
        entityManager.persist(bank)
        entityManager.flush()

    def findBank(self):
        id = vars.get('id')
        return self.findBankById(id)

    def findBankById(self, id):
        return entityManager.createQuery('Select bank From Bank bank Where bank.id = ' + str(id)).getSingleResult()
    
    def findBankByKey(self, key):
        return entityManager.createQuery('Select bank From Bank bank Where bank.key = ' + str(key)).getSingleResult()
