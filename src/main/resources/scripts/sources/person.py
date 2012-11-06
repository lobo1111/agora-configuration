from pl.reaper.container.data import Address
from pl.reaper.container.data import Person

class PersonManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        person = Person()
        person.setFirstName(vars.get('firstName'))
        person.setLastName(vars.get('lastName'))
        person.setNip(vars.get('nip'))
        person.setPesel(vars.get('pesel'))
        person.setEmail(vars.get('email'))
        person.setPhoneNumber1(vars.get('phone1'))
        person.setPhoneNumber2(vars.get('phone2'))
        person.setPhoneNumber3(vars.get('phone3'))
        person.setAddress(self.getAddress())
        self.savePerson(person)
        
    def getAddress(self):
        address = Address()
        address.setStreet(vars.get('street'))
        address.setHouseNumber(vars.get('houseNumber'))
        address.setFlatNumber(vars.get('flatNumber'))
        address.setPostalCode(vars.get('postal'))
        address.setCity(vars.get('city'))
        self.saveAddress(address)
        return address
    
    def saveAddress(self, address):
        self._logger.info(address.longDescription())
        entityManager.persist(address)
        entityManager.flush()
        
    def savePerson(self, person):
        self._logger.info(person.longDescription())
        entityManager.persist(person)
        entityManager.flush()