class PossessionManager(Container):
    _logger = Logger([:_scriptId])
    
    def addPersonOwner(self):
        person = self.findPerson();
        possession = self.findPossession()
        if not self.hasBound(person, possession):
            self._logger.info('Creating new bound: [person:%d]<->[possession:%d]' % (person.getId(), possession.getId()));
            possession.getPeople().add(person)
            entityManager.persist(possession)
        else:
            self._logger.info('Bound allready exists: [person:%d]<->[possession:%d]' % (person.getId(), possession.getId()));
        
    def hasBound(self, toBound, possession):
        for person in possession.getPeople():
            if(toBound.getId() == person.getId()):
                return True
        return False
        
    def findPerson(self):
        id = vars.get('owner')
        return entityManager.createQuery('Select person From Person person Where person.id = ' + id).getSingleResult()
    
    def findPossession(self):
        id = vars.get('possession')
        return entityManager.createQuery('Select possession From Possession possession Where possession.id = ' + id).getSingleResult()