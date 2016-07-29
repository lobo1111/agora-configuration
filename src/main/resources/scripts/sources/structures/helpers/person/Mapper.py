from structures.Address import AddressManager
from structures.helpers.common.Mapper import Mapper
from pl.reaper.container.data import Person
from structures.validators.common.LengthValidator import LengthValidator

class PersonMapper(Mapper):

    def extractOrCreatePerson(self, entity):
        if entity.getPerson() is not None:
            self._logger.info("Person extraction - person found id: %d" % entity.getPerson().getId())
            self._entity = entity.getPerson()
        else:
            self._logger.info("Person extraction - person not found, creating...")
            self._entity = Person()
        return self._entity
        
    def findOrCreate(self):
        if int(self._svars.get('id')) > 0:
            self._logger.info("Person lookup - found id: %s" % self._svars.get('id'))
            self._entity = self.findById("Person", int(self._svars.get('id')))
        else:
            self._logger.info("Person lookup - it's a new structure")
            self._entity = Person()
        return self._entity
        
    def setData(self):
        self.map("firstName", [LengthValidator(minLength = 1, maxLength = 150, messageParameter = self._label.get('field.firstName'))])
        self.map("lastName", [LengthValidator(minLength = 1, maxLength = 150, messageParameter = self._label.get('field.lastName'))])
        self.map("email", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.email'))])
        self.map("phoneNumber1", [LengthValidator(maxLength = 150, messageParameter = self._label.get('field.phoneNumber1'))])
        AddressManager().set(self._entity)