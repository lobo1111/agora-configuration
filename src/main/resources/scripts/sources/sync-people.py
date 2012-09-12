from pl.reaper.container.data import Address
from pl.reaper.container.data import Person
from java.math import BigDecimal

class SyncPeople(Sync):
    _logger = Logger([:_scriptId])
    _processed = 0
    _inserted = 0
    _updated = 0
    
    def sync(self):
        self._logger.info('synchronizing people')
        people = self.loadData('SELECT w FROM Platnicy w WHERE w.nazwa = "None"')
        for person in people:
            self._processed += 1
            self._logger.info('processing person %s' % person.getPlatnik())
            if self.personExists(person):
                self._logger.info('person exists, updating')
                self.personUpdate(person)
                self._updated += 1
            else:
                self._logger.info('person doesn\'t exists, inserting')
                self.personInsert(person)
                self._inserted += 1
        self._logger.info('person synchronized[processed:%d][inserted:%d][updated:%d]' % (self._processed, self._inserted, self._updated))

    def personExists(self, person):
        return self.syncDataExists('sync_person', 'access_person_id', person.getId())
    
    def personUpdate(self, oldPerson):
        id = self.findBaseId('sync_person', 'erp_person_id', 'access_person_id', oldPerson.getId())
        person = self.find('Person', id)
        self.setDataAndPersistPerson(oldPerson, pserson)
    
    def personInsert(self, oldPerson):
        person = Person()
        self.setDataAndPersistPerson(oldPerson, person)
        self._logger.info('new person bound: %d <-> %d' % (oldPerson.getId(), person.getId()))
        entityManager.createNativeQuery('INSERT INTO sync_person(`erp_person_id`, `access_person_id`) VALUES(%d, %d)' % (person.getId(), oldPerson.getId())).executeUpdate()
        
    def setDataAndPersistPerson(self, oldPerson, person):
        self.setAddress(oldPerson, person)
        self.setPerson(oldPerson, person)
        entityManager.flush()
        
    def setAddress(self, oldPerson, person):
        address = None
        if person.getAddress() != None:
            address = person.getAddress()
        else:
            address = Address()
        address.setStreet(self.findStreet(oldPerson.getKul()))
        address.setHouseNumber(oldPerson.getNrbr())
        address.setFlatNumber(oldPerson.getNrmie())
        address.setPostalCode(oldPerson.getKod())
        address.setCity('Swidnica')
        entityManager.persist(address)
        person.setAddress(address)
    
    def setPerson(self, oldPerson, person):
        person.setLastName(oldPerson.getNazwisko())
        person.setFirstName(oldPerson.getImie())
        person.setPhoneNumber1(oldPerson.getTel())
        person.setNip(oldPerson.getNip())
        entityManager.persist(person)
     