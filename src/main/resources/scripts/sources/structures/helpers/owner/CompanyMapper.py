from pl.reaper.container.data import Owner
from structures.helpers.common.Mapper import Mapper
from structures.Company import CompanyManager

class CompanyMapper(Mapper):
    
    def initStructure(self):
        self._entity = Owner()
    
    def setData(self):
        CompanyManager().set(self._entity)
        
    