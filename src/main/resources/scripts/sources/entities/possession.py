from pl.reaper.container.data import Person
from pl.reaper.container.data import Possession
from java.math import BigDecimal

class PossessionManager(Container):
    _logger = Logger([:_scriptId])
    
    def addPersonOwner(self):
        person = self.findPerson();
        possession = self.findPossession()
        if not self.hasPersonBound(person, possession):
            self._logger.info('Creating new bound: [person:%d]<->[possession:%d]' % (person.getId(), possession.getId()));
            possession.getPeople().add(person)
            entityManager.persist(possession)
        else:
            self._logger.info('Bound already exists: [person:%d]<->[possession:%d]' % (person.getId(), possession.getId()));
            
    def addCompanyOwner(self):
        company = self.findCompany();
        possession = self.findPossession()
        if not self.hasCompanyBound(company, possession):
            self._logger.info('Creating new bound: [company:%d]<->[possession:%d]' % (company.getId(), possession.getId()));
            possession.getCompanies().add(company)
            entityManager.persist(possession)
        else:
            self._logger.info('Bound already exists: [company:%d]<->[possession:%d]' % (company.getId(), possession.getId()));
            
    def removePersonOwner(self):
        person = self.findPerson();
        possession = self.findPossession()
        possession.getPeople().remove(person)
        entityManager.persist(possession)
            
    def removeCompanyOwner(self):
        company = self.findCompany();
        possession = self.findPossession()
        possession.getCompanies().remove(company)
        entityManager.persist(possession)
            
    def hasPersonBound(self, toBound, possession):
        return self.hasBound(toBound, possession.getPeople())
    
    def hasCompanyBound(self, toBound, possession):
        return self.hasBound(toBound, possession.getCompanies())
    
    def hasBound(self, toBound, entities):
        for entity in entities:
            if(toBound.getId() == entity.getId()):
                return True
        return False
        
    def findPerson(self):
        return self.find(('Select person From Person person Where person.id = %s' % vars.get('owner')))
    
    def findCompany(self):
        return self.find(('Select company From Company company Where company.id = %s' % vars.get('owner')))
    
    def findPossession(self):
        return self.find(('Select possession From Possession possession Where possession.id = %s' % vars.get('possession')))
    
    def find(self, query):
        return entityManager.createQuery(query).getSingleResult()
    
    def create(self):
        possession = Possession()
        self.setPossessionData(possession)
        self.savePossession(possession)
        
    def update(self):
        possession = self.findPossessionById()
        self.setPossessionData(possession)
        self.savePossession(possession)
        
    def setPossessionData(self, possession):
        possession.setArea(BigDecimal(vars.get('possessionArea')))
        possession.setShare(BigDecimal(vars.get('possessionShare')))
        possession.setAddress(self.getAddress(possession))
        possession.setCommunity(self.getCommunity(possession))
        
    def getAddress(self, possession):
        addressManager = AddressManager()
        return addressManager.getAddress(possession)

    def getCommunity(self, possession):
        communityManager = CommunityManager()
        return communityManager.findCommunityById(vars.get('communityId'))
        
    def savePossession(self, possession):
        self._logger.info(possession.longDescription())
        entityManager.persist(possession)
        entityManager.flush()
        
    def findPossessionById(self):
        id = vars.get('id')
        return entityManager.createQuery('Select possession From Possession possession Where possession.id = ' + id).getSingleResult()