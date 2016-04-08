from pl.reaper.container.data import Possession
from structures.Address import AddressManager
from structures.helpers.common.Mapper import Mapper
from structures.validators.common.DecimalValidator import DecimalValidator

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
            return self._entity

    def setData(self):
        AddressManager().set(self._entity)
        self.mapDecimal("area", [DecimalValidator(messageParameter=self._label.get('field.area'))])
        self.mapDecimal("declaredArea", [DecimalValidator(messageParameter=self._label.get('field.bookArea'))], self._entity.getAdditionalData())
        self.mapDecimal("declaredShare", [DecimalValidator(messageParameter=self._label.get('field.bookShare'))], self._entity.getAdditionalData())
        self.mapDecimal("people", [DecimalValidator(messageParameter=self._label.get('field.people'))], self._entity.getAdditionalData())
        self.mapDecimal("hotWater", [DecimalValidator(messageParameter=self._label.get('field.hotWater'))], self._entity.getAdditionalData())
        self.mapDecimal("coldWater", [DecimalValidator(messageParameter=self._label.get('field.coldWater'))], self._entity.getAdditionalData())
        self.mapDecimal("heat", [DecimalValidator(messageParameter=self._label.get('field.heat'))], self._entity.getAdditionalData())
        self.mapDecimal("heatArea", [DecimalValidator(messageParameter=self._label.get('field.heatArea'))], self._entity.getAdditionalData())
    
    def isNew(self):
        return self._isNewStructure
        