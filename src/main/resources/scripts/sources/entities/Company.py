from pl.reaper.container.data import Company
from base.Container import Container
from entities.Address import AddressManager

class CompanyManager(Container):
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix
    
    def create(self):
        company = Company()
        self.setCompanyData(company)
        self.saveCompany(company)
        return company
        
    def update(self):
        
        company = self.findCompanyById(self._svars.get(self._prefix + 'id'))
        self.setCompanyData(company)
        self.saveCompany(company)
        return company
    
    def toggleDefault(self):
        
        company = self.findCompanyById(self._svars.get(self._prefix + 'id'))
        company.setDefaultContractor(not company.isDefaultContractor())
        self.saveCompany(company)
        
    def setCompanyData(self, company):
        
        company.setName(self._svars.get(self._prefix + 'name'))
        company.setNip(self._svars.get(self._prefix + 'nip'))
        company.setRegon(self._svars.get(self._prefix + 'regon'))
        company.setEmail(self._svars.get(self._prefix + 'email'))
        company.setWww(self._svars.get('www'))
        company.setPhoneNumber1(self._svars.get(self._prefix + 'phoneNumber1'))
        company.setPhoneNumber2(self._svars.get(self._prefix + 'phoneNumber2'))
        company.setPhoneNumber3(self._svars.get(self._prefix + 'phoneNumber3'))
        company.setAddress(self.getAddress(company))
        
    def getAddress(self, person):
        addressManager = AddressManager()
        addressManager.setPrefix(self._prefix)
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