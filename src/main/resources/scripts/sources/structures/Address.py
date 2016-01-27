from pl.reaper.container.data import Address
from base.Container import Container

class AddressManager(Container):

    def set(self, entity):
        address = self.extractOrCreateAddress(entity)
        self.setData(address)
        entity.setAddress(address)
    
    def setData(self, address):
        address.setStreet(self._svars.get('street'))
        address.setHouseNumber(self._svars.get('houseNumber'))
        address.setFlatNumber(self._svars.get('flatNumber'))
        address.setPostalCode(self._svars.get('postalCode'))
        address.setCity(self._svars.get('city'))
        
    def extractOrCreateAddress(self, entity):
        if entity.getAddress() is not None:
            return entity.getAddress()
        else:
            return Address()