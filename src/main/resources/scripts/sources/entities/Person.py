from pl.reaper.container.data import Person
from base.Container import Container
from entities.Address import AddressManager

class PersonManager(Container):
    
    def create(self):
        person = Person()
        self.setPersonData(person)
        self.savePerson(person)
        return person
        
    def update(self):
        person = self.findPersonById(self._svars.get('id'))
        self.setPersonData(person)
        self.savePerson(person)
        return person
        
    def setPersonData(self, person):
        person.setFirstName(self._svars.get('firstName'))
        person.setLastName(self._svars.get('lastName'))
        person.setNip(self._svars.get('nip'))
        person.setPesel(self._svars.get('pesel'))
        person.setEmail(self._svars.get('email'))
        person.setPhoneNumber1(self._svars.get('phoneNumber1'))
        person.setPhoneNumber2(self._svars.get('phoneNumber2'))
        person.setPhoneNumber3(self._svars.get('phoneNumber3'))
        person.setAddress(self.getAddress(person))
        
    def getAddress(self, person):
        addressManager = AddressManager()
        addressManager.setEntityManager(self._entityManager)
        return addressManager.getAddress(person)
        
    def savePerson(self, person):
        self._logger.info(person.longDescription())
        self._entityManager.persist(person)
        self._entityManager.flush()
        
    def findPersonById(self, id):
        return self._entityManager.createQuery('Select person From Person person Where person.id = ' + id).getSingleResult()