from structures.Address import AddressManager
from structures.helpers.common.Mapper import Mapper
from pl.reaper.container.data import Company
from structures.validators.common.LengthValidator import LengthValidator

class CompanyMapper(Mapper):

    def extractOrCreateCompany(self, entity):
        if entity.getCompany() is not None:
            self._logger.info("Company extraction - company found id: %d" % entity.getCompany().getId())
            self._entity = entity.getCompany()
        else:
            self._logger.info("Company extraction - company not found, creating...")
            self._entity = Company()
        return self._entity
        
    def findOrCreate(self):
        if self._svars.get('id') != '0':
            self._logger.info("Company lookup - found id: %s" % self._svars.get('id'))
            self._entity = self.findById("Company", int(self._svars.get('id')))
        else:
            self._logger.info("Company lookup - it's a new structure")
            self._entity = Company()
        return self._entity
        
    def setData(self):
        self.map("name", [LengthValidator(minLength = 1, maxLength = 150, messageParameter = "Nazwa firmy")])
        self.map("nip", [LengthValidator(maxLength = 150, messageParameter = "NIP")])
        self.map("regon", [LengthValidator(maxLength = 150, messageParameter = "REGON")])
        self.map("email", [LengthValidator(maxLength = 150, messageParameter = "e-mail")])
        self.map("www", [LengthValidator(maxLength = 150, messageParameter = "WWW")])
        self.map("phone1", [LengthValidator(maxLength = 150, messageParameter = "Numer telefonu 1")])
        self.map("phone2", [LengthValidator(maxLength = 150, messageParameter = "Numer telefonu 2")])
        self.map("phone3", [LengthValidator(maxLength = 150, messageParameter = "Numer telefonu 3")])
        AddressManager().set(self._entity)