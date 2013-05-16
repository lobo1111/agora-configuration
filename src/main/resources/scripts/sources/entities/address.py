from pl.reaper.container.data import Address

class AddressManager(Container):
    _logger = Logger([:_scriptId])
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix

    def getAddress(self, entity):
        address = self.getOrCreateAddress(entity)
        self.setAddressData(address)
        self.saveAddress(address)
        return address
    
    def setAddressData(self, address):
        address.setStreet(vars.get(self._prefix + 'street'))
        address.setHouseNumber(vars.get(self._prefix + 'houseNumber'))
        address.setFlatNumber(vars.get(self._prefix + 'flatNumber'))
        address.setPostalCode(vars.get(self._prefix + 'postalCode'))
        address.setCity(vars.get(self._prefix + 'city'))
        
    def getOrCreateAddress(self, entity):
        if entity.getAddress() is not None:
            return entity.getAddress()
        else:
            return Address()
    
    def saveAddress(self, address):
        self._logger.info(address.longDescription())
        entityManager.persist(address)
        entityManager.flush()