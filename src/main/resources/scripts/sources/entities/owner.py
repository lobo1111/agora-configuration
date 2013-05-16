from pl.reaper.container.data import Owner

class OwnerManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        for possession in self.getPossessions():
            owner = Owner()
            owner.setPossession(possession)
            self.setOwnerData(owner)
            self.saveOwner(owner)
            
    def getPossessions(self):
        possessions = []
        for i in range(int(vars.get('possessionsCount'))):
            possessionId = int(vars.get('possession' + str(i)))
            possessions.append(PossessionManager().findPossessionById(possessionId))
        return possessions
            
        
    def setOwnerData(self, owner):
        self.setSubjectData(owner)
        self.setAdditionalAddressData(owner)
        
    def setSubjectData(self, owner):
        if vars.get('personSubject') != 'true':
            if vars.get('newSubject') != 'true':
                vars.put('id', vars.get('personId'))
                person = PersonManager().create()
            else:
                person = PersonManager().update()
            owner.setPerson(person)
        else:
            if vars.get('newSubject') != 'true':
                vars.put('id', vars.get('companyId'))
                company = CompanyManager().create()
            else:
                company = CompanyManager().update()
            owner.setCompany(company)
            
    def setAdditionalAddressData(self, owner):
        if vars.get('additionalAddress') != 'true':
            addressManager = AddressManager()
            addressManager.setPrefix('additionalAddress_')
            addressManager.getAddress(owner)
            
    def getAddress(self, owner):
        addressManager = AddressManager()
        return addressManager.getAddress(owner)
        
    def saveOwner(self, owner):
        self._logger.info(owner.longDescription())
        entityManager.persist(owner)
        entityManager.flush()
        
    def findOwnerById(self, id):
        return entityManager.createQuery('Select owner From Owner owner Where owner.id = ' + id).getSingleResult()