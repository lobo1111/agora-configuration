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
        global svars
        account.setName(svars.get('accountName'))
        account.setNumber(svars.get('accountNumber'))
        account.setType(self.getType())
        account.setCommunity(self.findCommunityById(svars.get('communityId')))
        if svars.get('parentAccountId') != None and svars.get('parentAccountId') != '0':
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
                entityManager.persist(account.getCommunity())
        if account.getType().getKey() in ['DEFAULT', 'REPAIR_FUND']:
            zpk = zpkManager.generateZpkForCommunity(account.getCommunity(), 'REPAIR_FUND')
            zpk.setAccount(account)
            account.getZpks().add(zpk)
            if account.getType().getKey() == 'REPAIR_FUND' and account.getCommunity().getRepairFundAccount() == None:
                account.getCommunity().setRepairFundAccount(account)
                entityManager.persist(account.getCommunity())
        
    def getType(self):
        global svars
        return DictionaryManager().getDictionaryInstance(svars.get('accountTypeId'))
    
    def getParent(self):
        global svars
        return self.findAccountById(svars.get('parentAccountId'))
    
    def getBank(self):
        global svars
        return BankManager().findBankById(svars.get('bankId'))
        
    def saveAccount(self, account):
        self._logger.info(account.longDescription())
        entityManager.persist(account)
        entityManager.flush()

    def findAccount(self):
        global svars
        id = svars.get('id')
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
