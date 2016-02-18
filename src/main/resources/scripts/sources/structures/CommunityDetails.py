from base.Container import Container
from structures.helpers.community.Mapper import CommunityMapper
from structures.Zpk import ZpkManager
from structures.Element import ElementManager
from structures.Contractor import ContractorManager
from structures.validators.common.ValidationError import ValidationError
from java.util import Date 

class CommunityDetailsManager(Container):
    _mapper = CommunityMapper()

    def persist(self):
        try:
            self._mapper.initStructure()
            self._mapper.setData()
            if self._mapper.isNew():
                self.createZpkNumbers(community)
                self.createElements(community)
                self.createContractors(community)
            self.saveEntity(community)
        except ValidationError, e:
            self.setError(e)
    
    def activate(self):
        community = self.findById("Community", self._svars.get('id'))
        if community.getInDate() == None and community.getOutDate() == None:
            community.setInDate(Date())
        self.saveEntity(community)
        
    def deactivate(self):
        community = self.findById("Community", self._svars.get('id'))
        if community.getInDate() != None and community.getOutDate() == None:
            community.setOutDate(Date())
        self.saveEntity(community)
        
    def createZpkNumbers(self, community):
        ZpkManager().createDefaultZpkNumbersForCommunity(community)
        
    def createElements(self, community):        
        ElementManager().createDefaultElementsForCommunity(community)
        
    def createContractors(self, community):
        ContractorManager().createDefaultContractorsForCommunity(community)
        