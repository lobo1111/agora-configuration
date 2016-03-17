from structures.helpers.common.Mapper import Mapper
from structures.helpers.element.GlobalMapper import GlobalMapper
from structures.helpers.element.CommunityMapper import CommunityMapper
from structures.helpers.element.PossessionMapper import PossessionMapper

class ElementMapper(Mapper):
    
    def initStructure(self):
        if int(self.get('id')) > 0:
            self._logger.info("Element persist - it's an update. Found id: %s, of type %s" % (self.get('id'), self.get('type')))
            self._mapper = self.getSpecializedMapper()
            self._mapper._isNew = False
            self._mapper.loadEntity()
        else:
            self._logger.info("Element persist - it's a new element")
            self._mapper = GlobalMapper()
            self._mapper._isNew = True
            self._mapper.setSpecializedMapper(self.getSpecializedMapper(skipGlobal = True))
            self._mapper.initStructure()
            
    def setData(self):
        self._mapper.setData()
        
    def getSpecializedMapper(self, skipGlobal = False):
        if self.get('type') == 'GLOBAL' and not skipGlobal:
            return GlobalMapper()
        elif self.get('type') == 'COMMUNITY':
            return CommunityMapper()
        elif self.get('type') == 'POSSESSION':
            return PossessionMapper()
        else:
            return None
        
    def getEntity(self):
        if self._mapper._isNew and self._mapper.getSpecializedMapper() != None:
            return self._mapper.getSpecializedMapper().getEntity()
        else:
            return self._mapper.getEntity()