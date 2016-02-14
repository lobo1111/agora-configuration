from structures.common.Mapper import Mapper
from structures.helpers.account.BankDataHelper import BankDataHelper
from pl.reaper.container.data import Account

class AccountMapper(Mapper):
    
    def __init__(self):
        if self._svars.get('id') != '0':
            self._logger.info("Account persist - it's an update. Found id: %s" % self._svars.get('id'))
            self._entity = self.findById("Account", int(self._svars.get('id')))
            self._isNew = False
        else:
            self._logger.info("Account persist - it's a new account")
            self._entity = Account()
            self._isNew = True
        BankDataHelper().handleData(self._entity)
        self.cacheNewType()
        
    def cacheNewType(self):
        self._newType = DictionaryManager().findByValue("ACCOUNT_TYPES", self._svars.get('type'))
        
    def setData(self):
        self.map("number")
        self.setCommunity()
        self.mapType()
        
    def mapType(self):
        self._entity.setType(self._newType)
        
    def getTypeValue(self):
        return self._svars.get('type')
    
    def getNewTypeKey(self):
        return self._newType.getKey()
        
    def typeChanged(self):
        return not self._entity.getType().equals(self._newTyp)
    
    def unsetType(self, account):
        unsetType = DictionaryManager().findDictionaryInstance("ACCOUNT_TYPES", "UNSET")
        account.setType(unsetType)