from pl.reaper.container.data import Owner
from base.Container import Container
from entities.Company import CompanyManager
from entities.Person import PersonManager
from entities.Address import AddressManager
from entities.Possession import PossessionManager

class OwnerManager(Container):
    
    def create(self):
        
        subject = self.getSubject()
        for possession in self.getPossessions():
            owner = Owner()
            owner.setPossession(possession)
            self.setSubject(owner, subject)
            additionalAddress = self.getAdditionalAddress()
            self.setAdditionalAddress(owner, additionalAddress)
            self.saveOwner(owner)
        if self._svars.get('newPossession') == 'true':
            self.createPossession(subject)
            
    def update(self):
        
        owner = self.findOwnerById(self._svars.get('id'))
        additionalAddress = self.getAdditionalAddress()
        self.setAdditionalAddress(owner, additionalAddress)
        self.saveOwner(owner)
        
    def delete(self):
        
        owner = self.findOwnerById(self._svars.get('id'))
        entityManager.remove(owner)

    def createPossession(self, subject):
        possessionManager = PossessionManager()
        possessionManager.setPrefix('newPossession_')
        possession = possessionManager.create()
        owner = Owner()
        owner.setPossession(possession)
        self.setSubject(owner, subject)
        additionalAddress = self.getAdditionalAddress()
        self.setAdditionalAddress(owner, additionalAddress)
        self.saveOwner(owner)
            
    def getPossessions(self):
        
        possessions = []
        for i in range(int(self._svars.get('possessionsCount'))):
            possessionId = self._svars.get('possession' + str(i))
            possessions.append(PossessionManager().findPossessionById(possessionId))
        return possessions
        
    def getSubject(self):
        
        if self._svars.get('personSubject') == 'true':
            if self._svars.get('newSubject') == 'true':
                return PersonManager().create()
            else:
                return PersonManager().findPersonById(self._svars.get('personId'))
        else:
            if self._svars.get('newSubject') == 'true':
                return CompanyManager().create()
            else:
                return CompanyManager().findCompanyById(self._svars.get('companyId'))
        
    def setSubject(self, owner, subject):
        
        if self._svars.get('personSubject') == 'true':
            owner.setPerson(subject)
        else:
            owner.setCompany(subject)
        subject.getOwners().add(owner)
            
    def getAdditionalAddress(self):
        
        if self._svars.get('additionalAddress') == 'true':
            addressManager = AddressManager()
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
        return AddressManager().getAddress(owner)
        
    def saveOwner(self, owner):
        self._logger.info(owner.longDescription())
        entityManager.persist(owner)
        entityManager.flush()
        
    def findOwnerById(self, id):
        return entityManager.createQuery('Select owner From Owner owner Where owner.id = ' + id).getSingleResult()