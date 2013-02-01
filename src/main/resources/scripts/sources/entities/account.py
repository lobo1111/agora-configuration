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
        account.setType(self.getType(account))
        account.setParrent(self.getParent(account))
        account.setBank(self.getBank(account))
        
    def setType(self, account):
        return DictionaryManager().getDictionaryInstance(vars.get('accountType'))
    
    def setParrent(self, account):
        return self.findAccountById(vars.get('parrentAccountId'))
    
    def setBank(self, account):
        bankManager = BankManager()
        return bankManager.findBankByKey(vars.get('bankKey'))
        
    def saveAccount(self, bank):
        self._logger.info(account.longDescription())
        entityManager.persist(account)
        entityManager.flush()

    def findAccount(self):
        id = vars.get('id')
        return self.findAccountById(id)

    def findAccountById(self, id):
        return entityManager.createQuery('Select account From Account account Where account.id = ' + str(id)).getSingleResult()
