from structures.helpers.common.Mapper import Mapper
from structures.helpers.owner.CompanyMapper import CompanyMapper
from structures.helpers.owner.PersonMapper import PersonMapper
from structures.validators.common.BindValidator import BindValidator

class OwnerMapper(Mapper):
    
    def initStructure(self):
        if self.get("type") == "PERSON":
            self._mapper = PersonMapper()
        elif self.get("type") == "COMPANY":
            self._mapper = CompanyMapper()
        self._mapper.initStructure()
        self._entity = self._mapper.getEntity()
        self._isNew = True
            
    def setData(self):
        self._mapper.setData()
        self.mapDictionary("possession", BindValidator(entity = "Possession", messageParameter=self._label.get('field.possession')))
        
    def getEntity(self):
        return self._mapper.getEntity()