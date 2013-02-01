from pl.reaper.container.data import Account

class AccountManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        account = Account()
        self.setAccountData(account)
        self.saveAccount(account)
        
    def update(self):
        account = self.findAccount()
        self.setAccountData(account)
        self.saveAccount(account)
        
    def setAccountData(self, account):
        account.setName(vars.get('accountName'))
        account.setNumber(vars.get('accountNumber'))
        account.setType(self.getType())
        account.setParrent(self.getParent())
        account.setBank(self.getBank())
        
    def getType(self):
        return DictionaryManager().getDictionaryInstance(vars.get('accountTypeId'))
    
    def getParrent(self):
        return self.findAccountById(vars.get('parrentAccountId'))
    
    def getBank(self):
        return BankManager().findBankByKey(vars.get('bankKey'))
        
    def saveAccount(self, bank):
        self._logger.info(account.longDescription())
        entityManager.persist(account)
        entityManager.flush()

    def findAccount(self):
        id = vars.get('id')
        return self.findAccountById(id)

    def findAccountById(self, id):
        return entityManager.createQuery('Select account From Account account Where account.id = ' + str(id)).getSingleResult()
