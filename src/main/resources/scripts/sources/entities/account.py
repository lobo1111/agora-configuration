from pl.reaper.container.data import Account

class AccountManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        account = Account()
        self.setAccountData(account)
        self.createZpk(account)
        self.saveAccount(account)
        
    def update(self):
        account = self.findAccount()
        self.setAccountData(account)
        self.saveAccount(account)
        
    def setAccountData(self, account):
        account.setName(vars.get('accountName'))
        account.setNumber(vars.get('accountNumber'))
        account.setType(self.getType())
        account.setCommunity(self.findCommunityById(vars.get('communityId')))
        if vars.get('parentAccountId') != None and vars.get('parentAccountId') != '0':
            account.setParrentAccount(self.getParent())
        account.setBank(self.getBank())
        
    def createZpk(self, account):
        if account.getType().getKey() in ['DEFAULT', 'REPAIR_FUND']:
            zpk = ZpkManager().generateZpkForCommunity(account.getCommunity(), account.getType().getKey())
            zpk.setAccount(account)
            account.setZpk(zpk)
            if account.getType().getKey() == 'DEFAULT' and account.getCommunity().getDefaultAccount() == None:
                account.getCommunity().setDefaultAccount(account)
            elif account.getType().getKey() == 'REPAIR_FUND' and account.getCommunity().getRepairAccount() == None:
                account.getCommunity().setRepairFundAccount(account)
        
    def getType(self):
        return DictionaryManager().getDictionaryInstance(vars.get('accountTypeId'))
    
    def getParent(self):
        return self.findAccountById(vars.get('parentAccountId'))
    
    def getBank(self):
        return BankManager().findBankById(vars.get('bankId'))
        
    def saveAccount(self, account):
        self._logger.info(account.longDescription())
        entityManager.persist(account)
        entityManager.flush()

    def findAccount(self):
        id = vars.get('id')
        return self.findAccountById(id)

    def findAccountById(self, id):
        return entityManager.createQuery('Select account From Account account Where account.id = ' + str(id)).getSingleResult()

    def findCommunityById(self, id):
        try:
            return entityManager.createQuery('Select c From Community c Where c.id = ' + str(id)).getSingleResult()
        except:
            return None

    def findAccountByNumber(self, number):
        sql = "Select account From Account account Where account.number = '%s'" % str(number)
        return entityManager.createQuery(sql).getSingleResult()
