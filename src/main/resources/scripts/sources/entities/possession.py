class PossessionManager(Container):
    _logger = Logger([:_scriptId])
    
    def addPersonOwner(self):
        person = self.findPerson();
        possession = self.findPossession()
        if not self.hasBound(person, possession):
            possession.getPeople().add(person)
            entityManager.persist(possession)
        
    def hasBound(self, toBound, possession):
        for person in possession.getPeople():
            if(toBound.getId() == person.getId()):
                return true
        return false
        
    def findPerson(self):
        id = vars.get('owner')
        return entityManager.createQuery('Select person From Person person Where person.id = ' + id).getSingleResult()
    
    def findPossession(self):
        id = vars.get('possession')
        return entityManager.createQuery('Select possession From Possession possession Where possession.id = ' + id).getSingleResult()