from pl.reaper.container.data import Address
from pl.reaper.container.data import Person

class PersonManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        person = Person()
        self.setPersonData(person)
        self.savePerson(person)
        
    def update(self):
        person = self.findPerson()
        self.setPersonData(person)
        self.savePerson(person)
        
    def setPersonData(self, person):
        person.setFirstName(vars.get('firstName'))
        person.setLastName(vars.get('lastName'))
        person.setNip(vars.get('nip'))
        person.setPesel(vars.get('pesel'))
        person.setEmail(vars.get('email'))
        person.setPhoneNumber1(vars.get('phoneNumber1'))
        person.setPhoneNumber2(vars.get('phoneNumber2'))
        person.setPhoneNumber3(vars.get('phoneNumber3'))
        person.setAddress(self.getAddress(person))
        
    def getAddress(self, person):
        address = self.getOrCreateAddress(person)
        self.setAddressData(address)
        self.saveAddress(address)
        return address
    
    def setAddressData(self, address):
        address.setStreet(vars.get('street'))
        address.setHouseNumber(vars.get('houseNumber'))
        address.setFlatNumber(vars.get('flatNumber'))
        address.setPostalCode(vars.get('postalCode'))
        address.setCity(vars.get('city'))
        
    def getOrCreateAddress(self, person):
        if person.getAddress() is not None:
            return person.getAddress()
        else:
            return Address()
    
    def saveAddress(self, address):
        self._logger.info(address.longDescription())
        entityManager.persist(address)
        entityManager.flush()
        
    def savePerson(self, person):
        self._logger.info(person.longDescription())
        entityManager.persist(person)
        entityManager.flush()
        
    def findPerson(self):
        id = vars.get('id')
        return entityManager.createQuery('Select person From Person person Where person.id = ' + id).getSingleResult()