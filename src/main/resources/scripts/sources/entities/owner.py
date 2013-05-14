from pl.reaper.container.data import Owner

class OwnerManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        owner = Owner()
        self.setOwnerData(owner)
        self.saveOwner(owner)
        
    def update(self):
        owner = self.findOwnerById(vars.get('id'))
        self.setOwnerData(owner)
        self.saveOwner(owner)
        
    def setOwnerData(self, owner):
        if vars.get('personId') is not None:
            person = PersonManager().findPersonById(vars.get('personId'))
            owner.setCompany(None)
            owner.setPerson(person)
        if vars.get('companyId') is not None:
            company = CompanyManager().findCompanyById(vars.get('companyId'))
            owner.setCompany(company)
            owner.setPerson(None)
        
    def getAddress(self, owner):
        addressManager = AddressManager()
        return addressManager.getAddress(owner)
        
    def saveOwner(self, owner):
        self._logger.info(owner.longDescription())
        entityManager.persist(owner)
        entityManager.flush()
        
    def findOwnerById(self, id):
        return entityManager.createQuery('Select owner From Owner owner Where owner.id = ' + id).getSingleResult()