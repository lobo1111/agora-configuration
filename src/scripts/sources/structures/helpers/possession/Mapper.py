from pl.reaper.container.data import Possession
from pl.reaper.container.data import PossessionAdditionalData
from structures.Address import AddressManager
from structures.helpers.common.Mapper import Mapper
from structures.validators.common.DecimalValidator import DecimalValidator
from structures.validators.common.IntValidator import IntValidator

class PossessionMapper(Mapper):
    
    def initStructure(self):
        if int(self.get('id')) > 0:
            self._logger.info("Possession persist - it's an update. Found id: %s" % self._svars.get('id'))
            self._entity = self.findById("Possession", int(self._svars.get('id')))
            self._isNewStructure = False
            return self._entity
        else:
            self._logger.info("Possession persist - it's a new possession")
            self._isNewStructure = True
            self._entity = Possession()
            additionalData = PossessionAdditionalData()
            additionalData.setPossession(self._entity)
            self._entity.setAdditionalData(additionalData)
            return self._entity

    def setData(self):
        self.mapDecimal("area", [DecimalValidator(messageParameter=self._label.get('field.area'))])
        self.map("declaredArea", [DecimalValidator(messageParameter=self._label.get('field.bookArea'))], self._entity.getAdditionalData())
        self.map("declaredShare", [DecimalValidator(messageParameter=self._label.get('field.bookShare'))], self._entity.getAdditionalData())
        self.map("people", [IntValidator(messageParameter=self._label.get('field.people'))], self._entity.getAdditionalData())
        self.map("hotWater", [DecimalValidator(messageParameter=self._label.get('field.hotWater'))], self._entity.getAdditionalData())
        self.map("coldWater", [DecimalValidator(messageParameter=self._label.get('field.coldWater'))], self._entity.getAdditionalData())
        self.map("heat", [DecimalValidator(messageParameter=self._label.get('field.heat'))], self._entity.getAdditionalData())
        self.map("heatArea", [DecimalValidator(messageParameter=self._label.get('field.heatArea'))], self._entity.getAdditionalData())
        AddressManager().set(self._entity)
        self.setCommunity()
    
    def isNew(self):
        return self._isNewStructure
        