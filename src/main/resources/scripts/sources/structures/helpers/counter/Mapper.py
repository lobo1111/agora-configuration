from pl.reaper.container.data import Counter
from pl.reaper.container.data import CounterStatus
from structures.helpers.common.Mapper import Mapper
from structures.validators.common.DictionaryValidator import DictionaryValidator
from structures.validators.common.LengthValidator import LengthValidator
from structures.validators.common.DecimalValidator import DecimalValidator
from structures.validators.common.BindValidator import BindValidator
from structures.validators.common.UniqueValidator import UniqueValidator
from structures.validators.common.NotNoneValidator import NotNoneValidator

class CounterMapper(Mapper):
    
    def initStructure(self):
        if int(self.get('id')) > 0:
            self._logger.info("Counter persist - it's a replace. Found id: %s" % self.get('id'))
            self._entity = self.findById("Counter", int(self.get('id')))
            self._isNew = False
        else:
            self._logger.info("Counter persist - it's a new counter")
            self._entity = Counter()
            self._isNew = True
    
    def setData(self):
        self.setCommunity()
        self.map("serialNumber", [UniqueValidator("Counter", "serialNumber", messageParameter=self._label.get('field.counterSerialNumber')), LengthValidator(minLength=1, maxLength=255, messageParameter=self._label.get('field.counterSerialNumber'))])
        self.map("seal", [LengthValidator(minLength=1, maxLength=255, messageParameter=self._label.get('field.counterSeal'))])
        self.mapDate("installation", [NotNoneValidator(messageParameter=self._label.get('field.installation'))])
        self.mapDictionary("legalization", DictionaryValidator(dictionary="YEARS", messageParameter=self._label.get('field.legalization')))
        if self.get("counterType") == "GLOBAL":
            self.mapDictionary("type", DictionaryValidator(dictionary="COUNTERS_TYPES", messageParameter=self._label.get('field.counterType')))
        if self.get("counterType") == "LOCAL":
            self.mapDictionary("parent", BindValidator(entity = "Counter", messageParameter=self._label.get('field.parentCounter')))
            self.mapDictionary("possession", BindValidator(entity = "Possession", messageParameter=self._label.get('field.possession')))
            self.getEntity().setType(self.getEntity().getParent().getType())
        self._entity.getStatuses().add(self.createStatus())
        
    def createStatus(self):
        status = CounterStatus()
        self._svars.put('timestamp', self.get('installation'))
        self._svars.put('status', self.get('startStatus'))
        self._svars.put('statusType', self.get('startStatusType'))
        self.mapDate("timestamp", [NotNoneValidator(messageParameter=self._label.get('field.installation'))], status)
        self.map("status", [DecimalValidator(messageParameter=self._label.get('field.counterStatus'))], status)
        status.setPredicted(False)
        status.setCounter(self._entity)
        return status
    
    def replace(self):
        self.map("seal", [LengthValidator(minLength=1, maxLength=255, messageParameter=self._label.get('field.counterSeal'))])
        self.mapDate("installation", [NotNoneValidator(messageParameter=self._label.get('field.installation'))])
        self.mapDictionary("legalization", DictionaryValidator(dictionary="YEARS", messageParameter=self._label.get('field.legalization')))
        oldCounter = self.findBy("Counter", "serialNumber", "'" + self.get("replacementOf") + "'")
        oldCounter.setDecomission(self._entity.getInstallation())
        self._entity.setCommunity(oldCounter.getCommunity())
        self._entity.setType(oldCounter.getType())
        self._entity.setPossession(oldCounter.getPossession())
        self._entity.setParent(oldCounter.getParent())
        self._entity.setReplacementOf(oldCounter)
        status = self.createStatus()
        self._entity.getStatuses().add(status)
        oldCounter.getStatuses().add(status)
        self.mapChildren(oldCounter, self._entity)
        
    def mapChildren(self, oldCounter, newCounter):
        for child in oldCounter.getChildren():
            child.setParent(newCounter)
            newCounter.getChildren(child)
        oldCounter().getChildren().clear()
        