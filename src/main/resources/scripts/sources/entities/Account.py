from pl.reaper.container.data import Account
from base.Container import Container
from entities.Bank import BankManager
from entities.Dictionary import DictionaryManager
from entities.Zpk import ZpkManager

class AccountManager(Container):
    
    def create(self):
        account = Account()
        self.setAccountData(account)
        if not account.getCommunity() is None:
            self.createZpk(account)
        self.saveAccount(account)
        
    def update(self):
        account = self.findAccount()
        self.setAccountData(account)
        self.saveAccount(account)

    def importCSV(self):
        from entities.Community import CommunityManager
        account = self.findOrCreate(self._svars.get('accountName'))
        if account.getCommunity() != None and account.getCommunity().getCompany().getName() != '' and account.getCommunity().getCompany().getName() != self._svars.get('communityName'):
            raise Exception('importer cannot change community !')
        account.setCommunity(CommunityManager().findByLabel(self._svars.get('communityName')))
        account.setNumber(self._svars.get('accountNumber'))
        account.setType(DictionaryManager().findByLabel('ACCOUNT_TYPE', self._svars.get('accountTypeValue')))
        if self._svars.get('parentAccountName') != '':
            account.setParrentAccount(self.findByLabel(self._svars.get('parentAccountName')))
        if account.getId() == 0:
            self.createZpk(account)
        else:
            pass
        account.setBank(BankManager().findByLabel(self._svars.get('name')))
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
        zpkManager.setEntityManager(self._entityManager)
        zpkManager.setSvars(self._svars)
        if account.getType().getKey() in ['DEFAULT', 'RENT']:
            zpk = zpkManager.generateZpkForCommunity(account.getCommunity(), 'RENT')
            zpkManager.setStartBalance(zpk, float(self._svars.get('startCredit')), float(self._svars.get('startDebit')))
            zpk.setAccount(account)
            account.getZpks().add(zpk)
            if account.getCommunity().getDefaultAccount() == None:
                account.getCommunity().setDefaultAccount(account)
                self._entityManager.persist(account.getCommunity())
        if account.getType().getKey() in ['DEFAULT', 'REPAIR_FUND']:
            zpk = zpkManager.generateZpkForCommunity(account.getCommunity(), 'REPAIR_FUND')
            zpkManager.setStartBalance(zpk, float(self._svars.get('startCredit')), float(self._svars.get('startDebit')))
            zpk.setAccount(account)
            account.getZpks().add(zpk)
            if account.getType().getKey() == 'REPAIR_FUND' and account.getCommunity().getRepairFundAccount() == None:
                account.getCommunity().setRepairFundAccount(account)
                self._entityManager.persist(account.getCommunity())
        
    def getType(self):
        manager = DictionaryManager()
        manager.setEntityManager(self._entityManager)
        manager.setSvars(self._svars)
        return manager.getDictionaryInstance(self._svars.get('accountTypeId'))
    
    def getParent(self):
        return self.findAccountById(self._svars.get('parentAccountId'))
    
    def getBank(self):
        manager = BankManager()
        manager.setEntityManager(self._entityManager)
        manager.setSvars(self._svars)
        return manager.findBankById(self._svars.get('bankId'))
        
    def saveAccount(self, account):
        self._logger.info(account.longDescription())
        self._entityManager.persist(account)
        self._entityManager.flush()

    def findAccount(self):
        id = self._svars.get('id')
        return self.findAccountById(id)

    def findByLabel(self, label):
        return self._entityManager.createQuery("Select a From Account a where a.name = '%s'" % label).getSingleResult()

    def findOrCreate(self, label):
        return self.findByLabel(label)
        #try:
        #except:
        #    account = Account()
        #    account.setName(label)
        #    return account

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
