from pl.reaper.container.data import Company

class CompanyManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        company = Company()
        self.setCompanyData(company)
        self.saveCompany(company)
        
    def update(self):
        company = self.findCompany()
        self.setCompanyData(company)
        self.saveCompany(company)
        
    def setCompanynData(self, company):
        company.setName(vars.get('name'))
        company.setNip(vars.get('nip'))
        company.setRegon(vars.get('regon'))
        company.setPesel(vars.get('pesel'))
        company.setEmail(vars.get('email'))
        company.setPhoneNumber1(vars.get('phoneNumber1'))
        company.setPhoneNumber2(vars.get('phoneNumber2'))
        company.setPhoneNumber3(vars.get('phoneNumber3'))
        company.setAddress(self.getAddress(company))
        
    def getAddress(self, person):
        addressManager = AddressManager()
        return addressManager.getAddress(person)
        
    def saveCompany(self, company):
        self._logger.info(person.longDescription())
        entityManager.persist(person)
        entityManager.flush()
        
    def findCompany(self):
        id = vars.get('id')
        return entityManager.createQuery('Select company From Company company Where company.id = ' + id).getSingleResult()