from pl.reaper.container.data import Company
from base.Container import Container
from structures.Address import AddressManager

class CompanyManager(Container):
    
    def set(self, entity):
        company = self.extractOrCreateCompany(entity)
        self.setData(company)
        entity.setCompany(company)
    
    def setData(self, company):
        company.setName(self._svars.get('name'))
        company.setNip(self._svars.get('nip'))
        company.setRegon(self._svars.get('regon'))
        company.setEmail(self._svars.get('email'))
        company.setWww(self._svars.get('www'))
        company.setPhoneNumber1(self._svars.get('phone1'))
        company.setPhoneNumber2(self._svars.get('phone2'))
        company.setPhoneNumber3(self._svars.get('phone3'))
        AddressManager().set(company)
    
    def extractOrCreateCompany(self, entity):
        if entity.getCompany() is not None:
            self._logger.info("Company extraction - company found id: %d" % entity.getCompany().getId())
            return entity.getCompany()
        else:
            self._logger.info("Company extraction - company not found, creating...")
            return Company()