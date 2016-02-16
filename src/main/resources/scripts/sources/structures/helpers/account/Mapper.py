from structures.Dictionary import DictionaryManager
from structures.helpers.common.Mapper import Mapper
from pl.reaper.container.data import Account

class AccountMapper(Mapper):
    
    def initStructure(self):
        if self.get('id') != '0':
            self._logger.info("Account persist - it's an update. Found id: %s" % self.get('id'))
            self._entity = self.findById("Account", int(self.get('id')))
            self._isNew = False
        else:
            self._logger.info("Account persist - it's a new account")
            self._entity = Account()
            self._isNew = True
        self.cacheNewType()
        
    def cacheNewType(self):
        self._newType = DictionaryManager().findByValue("ACCOUNT_TYPE", self.get('type'))
        
    def setData(self):
        self.map("number")
        self.setCommunity()
        self.mapType()
        
    def mapType(self):
        self._entity.setType(self._newType)
        
    def getTypeValue(self):
        return self.get('type')
    
    def getNewTypeKey(self):
        return self._newType.getKey()
        
    def typeChanged(self):
        return not self._entity.getType().equals(self._newTyp)
    
    def unsetType(self, account):
        unsetType = DictionaryManager().findDictionaryInstance("ACCOUNT_TYPE", "UNSET")
        account.setType(unsetType)