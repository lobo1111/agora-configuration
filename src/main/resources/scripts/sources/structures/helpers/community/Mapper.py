from structures.Company import CompanyManager
from structures.helpers.common.Mapper import Mapper
from structures.validators.community.UniqueCommunityNameValidator import UniqueCommunityNameValidator
from pl.reaper.container.data import Community

class CommunityMapper(Mapper):
    
    def initStructure(self):
        if self._svars.get('id') != '0':
            self._logger.info("Community persist - it's an update. Found id: %s" % self._svars.get('id'))
            self._entity = self.findById("Community", int(self._svars.get('id')))
            self._isNewStructure = False
            return self._entity
        else:
            self._logger.info("Community persist - it's a new community")
            self._isNewStructure = True
            self._entity = Community()
            return self._entity

    '''
    Mapping is not necessary in case of community name because it can't be longer
    than company name. Both attributes has the same restriction - 1-150 chars.
    There is a LengthValidator set on company name already.
    '''
    def setData(self):
        self.map("name", [UniqueCommunityNameValidator()])
        self._entity.setName(self._entity.getShortName(self._entity.getName()))
        CompanyManager().set(self._entity)
            
    def isNew(self):
        return self._isNewStructure
        