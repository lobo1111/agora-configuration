from pl.reaper.container.data import Address

def AddressManager(Container):

    def getAddress(self, entity):
        address = self.getOrCreateAddress(entity)
        self.setAddressData(address)
        self.saveAddress(address)
        return address
    
    def setAddressData(self, address):
        address.setStreet(vars.get('street'))
        address.setHouseNumber(vars.get('houseNumber'))
        address.setFlatNumber(vars.get('flatNumber'))
        address.setPostalCode(vars.get('postalCode'))
        address.setCity(vars.get('city'))
        
    def getOrCreateAddress(self, entity):
        if entity.getAddress() is not None:
            return entity.getAddress()
        else:
            return Address()
    
    def saveAddress(self, address):
        self._logger.info(address.longDescription())
        entityManager.persist(address)
        entityManager.flush()