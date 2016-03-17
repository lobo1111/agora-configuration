from pl.reaper.container.data import ElementPossession
from structures.helpers.common.Mapper import Mapper
from structures.validators.common.DecimalValidator import DecimalValidator

class PossessionMapper(Mapper):
    
    def initStructure(self):
        self._entity = ElementPossession()
    
    def loadEntity(self):
        self._entity = self.findById("ElementPossession", self._svars.get('id'))
    
    def setData(self):
        self._entity.setCommunity(self.findById('Community', self._svars.get('communityId')))
        self.map("overrideParentValue")
        self.map("globalValue", [DecimalValidator(messageParameter=self._label.get('field.value'))])
    
    def bind(self, globalElement):
        globalElement.getPossessionElements().add(self._entity)
        self._entity.setElement(globalElement)