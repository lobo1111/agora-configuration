from pl.reaper.container.data import Company

class CompanyManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        company = Company()
        self.setCompanyData(company)
        self.saveCompany(company)
        
    def update(self):
        company = self.findCompanyById(vars.get('id'))
        self.setCompanyData(company)
        self.saveCompany(company)
        
    def setCompanyData(self, company):
        company.setName(vars.get('name'))
        company.setNip(vars.get('nip'))
        company.setRegon(vars.get('regon'))
        company.setEmail(vars.get('email'))
        company.setWww(vars.get('www'))
        company.setPhoneNumber1(vars.get('phoneNumber1'))
        company.setPhoneNumber2(vars.get('phoneNumber2'))
        company.setPhoneNumber3(vars.get('phoneNumber3'))
        company.setAddress(self.getAddress(company))
        
    def getAddress(self, person):
        addressManager = AddressManager()
        return addressManager.getAddress(person)
    
    def getCompany(self, entity):
        company = self.getOrCreateCompany(entity)
        self.setCompanyData(company)
        self.saveCompany(company)
        return company
    
    def getOrCreateCompany(self, entity):
        if entity.getCompany() is not None:
            return entity.getCompany()
        else:
            return Company()
        
    def saveCompany(self, company):
        self._logger.info(company.longDescription())
        entityManager.persist(company)
        entityManager.flush()
        
    def findCompanyById(self, id):
        return entityManager.createQuery('Select company From Company company Where company.id = ' + id).getSingleResult()