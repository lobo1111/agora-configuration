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
        if int(self._svars.get('id')) > 0:
            self._logger.info("Company lookup - found id: %s" % self._svars.get('id'))
            self._entity = self.findById("Company", int(self._svars.get('id')))
        else:
            self._logger.info("Company lookup - it's a new structure")
            self._entity = Company()
        return self._entity
        
    def setData(self):
        self.map("name", [LengthValidator(minLength = 1, maxLength = 150, messageParameter = self._label.get('field.companyName'))])
        self.map("nip", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.nip'))])
        self.map("regon", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.regon'))])
        self.map("email", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.email'))])
        self.map("www", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.www'))])
        self.map("phoneNumber1", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.phoneNumber1'))])
        self.map("phoneNumber2", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.phoneNumber2'))])
        self.map("phoneNumber3", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.phoneNumber3'))])
        AddressManager().set(self._entity)