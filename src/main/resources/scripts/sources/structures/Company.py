from base.Container import Container
from structures.helpers.company.Mapper import CompanyMapper

class CompanyManager(Container):
    _mapper = CompanyMapper()
    
    def set(self, entity):
        self._mapper.extractOrCreateCompany(entity)
        self._mapper.setData()
        entity.setCompany(self._mapper.getEntity())
        
    def getMapper(self):
        return self._mapper
    
    