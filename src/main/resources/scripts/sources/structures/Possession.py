from base.Container import Container
from structures.Element import ElementManager
from structures.Zpk import ZpkManager
from structures.helpers.possession.Mapper import PossessionMapper
from structures.validators.common.ValidationError import ValidationError

class PossessionManager(Container):
    _mapper = PossessionMapper()
    
    def persist(self):
        try:
            self._mapper.initStructure()
            self._mapper.setData()
            if self._mapper.isNew():
                self.createZpkNumbers(self._mapper.getEntity())
                self.createElements(self._mapper.getEntity())
            CommunityDetailsManager().recalculateShares(self._mapper.getEntity().getCommunity())
            self.saveEntity(self._mapper.getEntity())
        except ValidationError, e:
            self.setError(e)
            
    def createZpkNumbers(self, entity):
        ZpkManager().createZpksForPossession(entity)
    
    def createElements(self, entity):
        ElementManager().createDefaultElementsForPossession(entity)
        