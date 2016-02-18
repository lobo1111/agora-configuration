from base.Container import Container
from structures.helpers.address.Mapper import AddressMapper

class AddressManager(Container):
    _mapper = AddressMapper()

    def set(self, entity):
        self._mapper.extractOrCreateAddress(entity)
        self._mapper.setData()
        entity.setAddress(self._mapper.getEntity())
    