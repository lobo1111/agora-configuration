from base.Container import Container
from pl.reaper.container.data import Community
from structures.Company import CompanyManager
from structures.Zpk import ZpkManager

class CommunityDetailsManager(Container):

    def persist(self):
        (community, isNewStructure) = self.initStructure()
        community.setInDate(self.parseDate(self._svars.get('inDate')))
        CompanyManager().set(community)
        if isNewStructure:
            self.createZpkNumbers(community)
            self.createElements(community)
            self.createContractors(community)
        self.saveEntity(community)
        return community
    
    def initStructure(self):
        if self._svars.get('id') != '0':
            return self.findById("Community", int(self._svars.get('id'))), False
        else:
            return Community(), True
        
    def createZpkNumbers(self, community):
        ZpkManager().createDefaultZpkNumbersForCommunity(community)
        
    def createElements(self, community):        
        ElementManager().createDefaultElementsForCommunity(community)
        
    def createContractors(self, community):
        ContractorManager().createDefaultContractorsForCommunity(community)
        