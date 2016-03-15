from structures.helpers.common.Mapper import Mapper
from structures.validators.common.LengthValidator import LengthValidator
from pl.reaper.container.data import Address

class AddressMapper(Mapper):
    
    def setData(self):
        self.map("street", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.street'))])
        self.map("houseNumber", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.houseNumber'))])
        self.map("flatNumber", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.flatNumber'))])
        self.map("postalCode", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.postalCode'))])
        self.map("city", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.city'))])
        
    def extractOrCreateAddress(self, entity):
        if entity.getAddress() is not None:
            self._logger.info("Address extraction - address found id: %d" % entity.getAddress().getId())
            self._entity = entity.getAddress()
            return self._entity
        else:
            self._logger.info("Address extraction - address not found, creating...")
            self._entity = Address()
            return self._entity

    