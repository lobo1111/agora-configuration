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
            
    def addCompanyOwner(self):
        company = self.findCompany();
        possession = self.findPossession()
        if not self.hasCompanyBound(company, possession):
            self._logger.info('Creating new bound: [company:%d]<->[possession:%d]' % (company.getId(), possession.getId()));
            possession.getCompanies().add(company)
            entityManager.persist(possession)
        else:
            self._logger.info('Bound allready exists: [company:%d]<->[possession:%d]' % (company.getId(), possession.getId()));
        
    def hasPeopleBound(self, toBound, possession):
        for person in possession.getPeople():
            if(toBound.getId() == person.getId()):
                return True
        return False
    
    def hasPeopleBound(self, toBound, possession):
        for company in possession.getCompanies():
            if(toBound.getId() == company.getId()):
                return True
        return False
        
    def findPerson(self):
        id = vars.get('owner')
        return entityManager.createQuery('Select person From Person person Where person.id = ' + id).getSingleResult()
    
    def findCompany(self):
        id = vars.get('owner')
        return entityManager.createQuery('Select company From Company company Where company.id = ' + id).getSingleResult()
    
    def findPossession(self):
        id = vars.get('possession')
        return entityManager.createQuery('Select possession From Possession possession Where possession.id = ' + id).getSingleResult()