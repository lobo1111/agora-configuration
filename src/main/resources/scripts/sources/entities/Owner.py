from pl.reaper.container.data import Owner
from base.Container import Container
from entities.Company import CompanyManager
from entities.Person import PersonManager
from entities.Address import AddressManager
from entities.Possession import PossessionManager

class OwnerManager(Container):
    
    def create(self):
        subject = self.getSubject()
        owner = Owner()
        self.setPossession(owner, self._svars.get('possessionId'));
        self.setSubject(owner, subject)
        additionalAddress = self.getAdditionalAddress()
        self.setAdditionalAddress(owner, additionalAddress)
        self.saveOwner(owner)
            
    def update(self):
        owner = self.findOwnerById(self._svars.get('id'))
        additionalAddress = self.getAdditionalAddress()
        self.setAdditionalAddress(owner, additionalAddress)
        self.saveOwner(owner)
        
    def delete(self):
        owner = self.findOwnerById(self._svars.get('id'))
        self._entityManager.remove(owner)

    def setPossession(self, owner, possessionId):
        possession = PossessionManager().findPossessionById(possessionId)
        owner.setPossession(possession)
        possession.getOwners().add(owner)
        self._entityManager.persist(possession)

    def getSubject(self):
        if self._svars.get('personSubject') == 'true':
            manager = PersonManager()
            return manager.findPersonById(self._svars.get('personId'))
        else:
            manager = CompanyManager()
            return manager.findCompanyById(self._svars.get('companyId'))
        
    def setSubject(self, owner, subject):
        if self._svars.get('personSubject') == 'true':
            owner.setPerson(subject)
        else:
            owner.setCompany(subject)
        subject.getOwners().add(owner)
            
    def getAdditionalAddress(self):
        if self._svars.get('additionalAddress') == 'true':
            addressManager = AddressManager()
            addressManager.setSvars(self._svars)
            addressManager.setEntityManager(self._entityManager)
            addressManager.setPrefix('additionalAddress_')
            return addressManager.getAddress(Owner())
        else:
            return None
        
    def setAdditionalAddress(self, owner, additionalAddress):
        if self._svars.get('additionalAddress') == 'true':
            owner.setAddress(additionalAddress)
        else:
            owner.setAddress(None)
            
    def getAddress(self, owner):
        addressManager = AddressManager()
        addressManager.setSvars(self._svars)
        addressManager.setEntityManager(self._entityManager)
        return addressManager.getAddress(owner)
        
    def saveOwner(self, owner):
        self._logger.info(owner.longDescription())
        self.saveEntity(owner)
        
    def findOwnerById(self, id):
        self._logger.info('Looking for owner with ID: %s' % str(id))
        print 'Looking for owner with ID: %s' % str(id)
        return self._entityManager.createQuery('Select owner From Owner owner Where owner.id = ' + id).getSingleResult()