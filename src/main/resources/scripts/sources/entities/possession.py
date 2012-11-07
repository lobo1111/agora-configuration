class PossessionManager(Container):
    _logger = Logger([:_scriptId])
    
    def addPersonOwner(self):
        person = self.findPerson();
        possession = self.findPossession()
        possession.getPeople().add(person)
        entityManager.persist(possession)
        
    def findPerson(self):
        id = vars.get('owner')
        return entityManager.createQuery('Select person From Person person Where person.id = ' + id).getSingleResult()
    
    def findPossession(self):
        id = vars.get('possession')
        return entityManager.createQuery('Select possession From Possession possession Where possession.id = ' + id).getSingleResult()