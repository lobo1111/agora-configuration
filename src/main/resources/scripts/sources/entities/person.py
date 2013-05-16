from pl.reaper.container.data import Person

class PersonManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        person = Person()
        self.setPersonData(person)
        self.savePerson(person)
        return person
        
    def update(self):
        person = self.findPersonById(vars.get('id'))
        self.setPersonData(person)
        self.savePerson(person)
        return person
        
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
        addressManager = AddressManager()
        return addressManager.getAddress(person)
        
    def savePerson(self, person):
        self._logger.info(person.longDescription())
        entityManager.persist(person)
        entityManager.flush()
        
    def findPersonById(self, id):
        return entityManager.createQuery('Select person From Person person Where person.id = ' + id).getSingleResult()