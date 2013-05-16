from pl.reaper.container.data import Owner

class OwnerManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        subject = self.getSubject()
        additionalAddress = self.getAdditionalAddress()
        
        for possession in self.getPossessions():
            owner = Owner()
            owner.setPossession(possession)
            self.setSubject(owner, subject)
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
                person = PersonManager().create()
            else:
                vars.put('id', vars.get('personId'))
                person = PersonManager().update()
            return person
        else:
            if vars.get('newSubject') == 'true':
                company = CompanyManager().create()
            else:
                vars.put('id', vars.get('companyId'))
                company = CompanyManager().update()
            return company
        
    def setSubject(self, owner, subject):
        if vars.get('personSubject') == 'true':
            owner.setPerson(subject)
        else:
            owner.setCompany(subject)
            
    def getAdditionalAddress(self):
        if vars.get('additionalAddress') == 'true':
            addressManager = AddressManager()
            addressManager.setPrefix('additionalAddress_')
            return addressManager.getAddress(owner)
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