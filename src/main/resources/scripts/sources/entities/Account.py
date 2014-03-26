from pl.reaper.container.data import Account
from base.Container import Container
from entities.Bank import BankManager
from entities.Dictionary import DictionaryManager

class AccountManager(Container):
    
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
        
        account.setName(self._svars.get('accountName'))
        account.setNumber(self._svars.get('accountNumber'))
        account.setType(self.getType())
        account.setCommunity(self.findCommunityById(self._svars.get('communityId')))
        if self._svars.get('parentAccountId') != None and self._svars.get('parentAccountId') != '0':
            account.setParrentAccount(self.getParent())
        account.setBank(self.getBank())
        
    def createZpk(self, account):
        zpkManager = ZpkManager()
        if account.getType().getKey() in ['DEFAULT', 'RENT']:
            zpk = zpkManager.generateZpkForCommunity(account.getCommunity(), 'RENT')
            zpk.setAccount(account)
            account.getZpks().add(zpk)
            if account.getCommunity().getDefaultAccount() == None:
                account.getCommunity().setDefaultAccount(account)
                self._entityManager.persist(account.getCommunity())
        if account.getType().getKey() in ['DEFAULT', 'REPAIR_FUND']:
            zpk = zpkManager.generateZpkForCommunity(account.getCommunity(), 'REPAIR_FUND')
            zpk.setAccount(account)
            account.getZpks().add(zpk)
            if account.getType().getKey() == 'REPAIR_FUND' and account.getCommunity().getRepairFundAccount() == None:
                account.getCommunity().setRepairFundAccount(account)
                self._entityManager.persist(account.getCommunity())
        
    def getType(self):
        
        return DictionaryManager().getDictionaryInstance(self._svars.get('accountTypeId'))
    
    def getParent(self):
        
        return self.findAccountById(self._svars.get('parentAccountId'))
    
    def getBank(self):
        
        return BankManager().findBankById(self._svars.get('bankId'))
        
    def saveAccount(self, account):
        self._logger.info(account.longDescription())
        self._entityManager.persist(account)
        self._entityManager.flush()

    def findAccount(self):
        
        id = self._svars.get('id')
        return self.findAccountById(id)

    def findAccountById(self, id):
        return self._entityManager.createQuery('Select account From Account account Where account.id = ' + str(id)).getSingleResult()

    def findCommunityById(self, id):
        try:
            return self._entityManager.createQuery('Select c From Community c Where c.id = ' + str(id)).getSingleResult()
        except:
            return None

    def findAccountByNumber(self, number):
        sql = "Select account From Account account Where account.number = '%s'" % str(number)
        return self._entityManager.createQuery(sql).getSingleResult()
