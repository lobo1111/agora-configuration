from pl.reaper.container.data import Dictionary

class ZpksSettings:
    def update(self):
        self.persistDict('possessionId', 'POSSESSION')
        self.persistDict('possessionRepairId', 'POSSESSION_REPAIR_FUND')
        self.persistDict('accountId', 'RENT')
        self.persistDict('repairFundAccountId', 'REPAIR_FUND')
        self.persistDict('contractorId', 'CONTRACTOR')
        self.persistDict('contractorCostId', 'CONTRACTOR_COST')
        self.persistDict('chargingRentId', 'CHARGING_RENT')
        self.persistDict('chargingRepairFundId', 'CHARGING_REPAIR_FUND')
        
    def persistDict(self, idVariableName, dictName):
        global svars
        id = svars.get(idVariableName)
        dict = self.findOrCreateDict(dictName)
        dict.setValue(id)
        entityManager.persist(dict)
        
    def findOrCreateDict(self, name):
        try:
            return self.findDict(name)
        except:
            dict = Dictionary()
            dict.setKey(name)
            dict.setType(self.findSettingsType())
            return dict
    
    def findDict(self, dict):
        return entityManager.createQuery("SELECT dict FROM Dictionary dict JOIN dict.type dtype WHERE dtype.type = 'ZPKS_SETTINGS' AND dict.key = '%s'" % dict).getSingleResult()
    
    def findSettingsType(self):
        return entityManager.createQuery("SELECT dtype FROM DictionaryType dtype WHERE dtype.type = 'ZPKS_SETTINGS'").getSingleResult()