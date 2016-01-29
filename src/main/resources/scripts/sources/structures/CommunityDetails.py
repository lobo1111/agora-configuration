from base.Container import Container
from pl.reaper.container.data import Community
from structures.Company import CompanyManager
from structures.Zpk import ZpkManager
from structures.Element import ElementManager
from structures.Contractor import ContractorManager
from java.util import Date 

class CommunityDetailsManager(Container):

    def persist(self):
        (community, isNewStructure) = self.initStructure()
        community.setName(self._svars.get('name'))
        CompanyManager().set(community)
        if isNewStructure:
            community.setInDate(Date())
            self.createZpkNumbers(community)
            self.createElements(community)
            self.createContractors(community)
        self.saveEntity(community)
    
    def initStructure(self):
        if self._svars.get('id') != '0':
            self._logger.info("Community persist - it's an update. Found id: %s" % self._svars.get('id'))
            return self.findById("Community", int(self._svars.get('id'))), False
        else:
            self._logger.info("Community persist - it's a new community")
            return Community(), True
        
    def createZpkNumbers(self, community):
        ZpkManager().createDefaultZpkNumbersForCommunity(community)
        
    def createElements(self, community):        
        ElementManager().createDefaultElementsForCommunity(community)
        
    def createContractors(self, community):
        ContractorManager().createDefaultContractorsForCommunity(community)
        