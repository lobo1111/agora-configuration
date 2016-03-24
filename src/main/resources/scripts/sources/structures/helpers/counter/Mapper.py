from pl.reaper.container.data import Counter
from structures.helpers.common.Mapper import Mapper
from structures.validators.common.DictionaryValidator import DictionaryValidator
from structures.validators.common.LengthValidator import LengthValidator
from structures.validators.common.DecimalValidator import DecimalValidator
from structures.validators.common.BindValidator import BindValidator
from structures.validators.common.UniqueValidator import UniqueValidator

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
        self.map("serialNumber", [UniqueValidator("Counter", "serialNumber"), LengthValidator(minLength=1, maxLength=255, messageParameter=self._label.get('field.counterSerialNumber'))])
        self.map("seal", [LengthValidator(minLength=1, maxLength=255, messageParameter=self._label.get('field.counterSerialNumber'))])
        self.mapDate("installation", [LengthValidator(minLength=1, messageParameter=self._label.get('field.installation'))])
        self.mapDictionary("type", [DictionaryValidator(dictionary="COUNTERS_TYPES", messageParameter=self._label.get('field.counterType'))])
        self.mapDictionary("legalization", [DictionaryValidator(dictionary="YEARS", messageParameter=self._label.get('field.legalization'))])
        if self.get("counterType") == "LOCAL":
            self.mapDictionary("parent", [BindValidator(entity = "Counter", messageParameter=self._label.get('field.parentCounter'))])
            self.mapDictionary("possession", [BindValidator(entity = "Possession", messageParameter=self._label.get('field.possession'))])
        self._entity.getStatuses().add(self.createStatus())
        
    def createStatus(self):
        status = CounterStatus()
        self._svars.put('timestamp', self.get('installation'))
        self._svars.put('status', self.get('startStatus'))
        self.map("timestamp", [LengthValidator(minLength=1, messageParameter=self._label.get('field.installation'))], status)
        self.map("status", [DecimalValidator(messageParameter=self._label.get('field.counterStatus'))], status)
        status.setPredicted(False)
        status.setCounter(self._entity)
        return status
    
    def replace(self):
        pass