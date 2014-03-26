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
        if vars.get('newPossession') == 'true':
            self.createPossession(subject)
            
    def update(self):
        owner = self.findOwnerById(vars.get('id'))
        additionalAddress = self.getAdditionalAddress()
        self.setAdditionalAddress(owner, additionalAddress)
        self.saveOwner(owner)
        
    def delete(self):
        owner = self.findOwnerById(vars.get('id'))
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
        for i in range(int(vars.get('possessionsCount'))):
            possessionId = vars.get('possession' + str(i))
            possessions.append(PossessionManager().findPossessionById(possessionId))
        return possessions
        
    def getSubject(self):
        if vars.get('personSubject') == 'true':
            if vars.get('newSubject') == 'true':
                return PersonManager().create()
            else:
                return PersonManager().findPersonById(vars.get('personId'))
        else:
            if vars.get('newSubject') == 'true':
                return CompanyManager().create()
            else:
                return CompanyManager().findCompanyById(vars.get('companyId'))
        
    def setSubject(self, owner, subject):
        if vars.get('personSubject') == 'true':
            owner.setPerson(subject)
        else:
            owner.setCompany(subject)
        subject.getOwners().add(owner)
            
    def getAdditionalAddress(self):
        if vars.get('additionalAddress') == 'true':
            addressManager = AddressManager()
            addressManager.setPrefix('additionalAddress_')
            return addressManager.getAddress(Owner())
        else:
            return None
        
    def setAdditionalAddress(self, owner, additionalAddress):
        if vars.get('additionalAddress') == 'true':
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