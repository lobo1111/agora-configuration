from base.Container import Container
from structures.Possession import PossessionManager
from structures.helpers.owner.Mapper import OwnerMapper
from structures.validators.common.ValidationError import ValidationError

class OwnerManager(Container):
    _mapper = OwnerMapper()
    
    def persist(self):
        try:
            self._mapper.initStructure()
            self._mapper.setData()
            PossessionManager().refreshShortcuts(self._mapper.getEntity().getPossession())
            self.saveEntity(self._mapper.getEntity())
        except ValidationError, e:
            self.setError(e)
            
    def remove(self):
        self._mapper.initStructure()
        self.removeEntity(self._mapper.getEntity())