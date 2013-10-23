from pl.reaper.container.data import Dictionary

class ZpksSettings:
    def update(self):
        possessionId = vars.get('possessionId')
        possessionDict = self.findPossessionDict()
        possessionDict.setValue(possessionId)
        entityManager.persist(possessionDict)
        accountId = vars.get('accountId')
        accountDict = self.findAccountDict()
        accountDict.setValue(accountId)
        entityManager.persist(accountDict)
        repairFundAccountId = vars.get('repairFundAccountId')
        repairFundAccountDict = self.findRepairFundAccountDict()
        repairFundAccountDict.setValue(repairFundAccountId)
        entityManager.persist(repairFundAccountDict)
        
    def findPossessionDict(self):
        try:
            return self.findDict("POSSESSION")
        except:
            dict = Dictionary()
            dict.setKey("POSSESSION")
            dict.setType(self.findSettingsType())
            return dict
        
    def findAccountDict(self):
        try:
            return self.findDict("ACCOUNT")
        except:
            dict = Dictionary()
            dict.setKey("ACCOUNT")
            dict.setType(self.findSettingsType())
            return dict
        
    def findAccountDict(self):
        try:
            return self.findDict("REPAIR_FUND_ACCOUNT")
        except:
            dict = Dictionary()
            dict.setKey("REPAIR_FUND_ACCOUNT")
            dict.setType(self.findSettingsType())
            return dict
    
    def findDict(self, dict):
        return entityManager.createQuery("SELECT dict FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = 'ZPKS_SETTINGS' AND dict.key = '%s'" % dict).getSingleResult()
    
    def findSettingsType(self):
        return entityManager.createQuery("SELECT dtype FROM DictionaryType dtype WHERE dtype.type = 'ZPKS_SETTINGS'").getSingleResult()