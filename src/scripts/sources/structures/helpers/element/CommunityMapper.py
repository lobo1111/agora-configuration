from pl.reaper.container.data import ElementCommunity
from structures.helpers.common.Mapper import Mapper
from structures.validators.common.DecimalValidator import DecimalValidator

class CommunityMapper(Mapper):
    
    def initStructure(self):
        self._entity = ElementCommunity()
    
    def loadEntity(self):
        self._entity = self.findById("ElementCommunity", self._svars.get('id'))
    
    def setData(self):
        self._entity.setCommunity(self.findById('Community', self._svars.get('communityId')))
        self.map("overrideParentValue")
        self.map("localValue", [DecimalValidator(messageParameter=self._label.get('field.value'))])
    
    def bind(self, globalElement):
        globalElement.getCommunityElements().add(self._entity)
        self._entity.setElement(globalElement)