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
        person = self.findPersonById(svars.get('id'))
        self.setPersonData(person)
        self.savePerson(person)
        return person
        
    def setPersonData(self, person):
        person.setFirstName(svars.get('firstName'))
        person.setLastName(svars.get('lastName'))
        person.setNip(svars.get('nip'))
        person.setPesel(svars.get('pesel'))
        person.setEmail(svars.get('email'))
        person.setPhoneNumber1(svars.get('phoneNumber1'))
        person.setPhoneNumber2(svars.get('phoneNumber2'))
        person.setPhoneNumber3(svars.get('phoneNumber3'))
        person.setAddress(self.getAddress(person))
        
    def getAddress(self, person):
        addressManager = AddressManager()
        return addressManager.getAddress(person)
        
    def savePerson(self, person):
        self._logger.info(person.longDescription())
        entityManager.persist(person)
        entityManager.flush()
        
    def findPersonById(self, id):
        return entityManager.createQuery('Select person From Person person Where person.id = ' + id).getSingleResult()