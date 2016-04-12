from base.Container import Container
from java.math import BigDecimal
from java.util import Date
from structures.Contractor import ContractorManager
from structures.Element import ElementManager
from structures.Zpk import ZpkManager
from structures.helpers.community.Mapper import CommunityMapper
from structures.validators.common.ValidationError import ValidationError

class CommunityDetailsManager(Container):
    _mapper = CommunityMapper()

    def persist(self):
        try:
            self._mapper.initStructure()
            self._mapper.setData()
            if self._mapper.isNew():
                self.createZpkNumbers(self._mapper.getEntity())
                self.createElements(self._mapper.getEntity())
                self.createContractors(self._mapper.getEntity())
            self.saveEntity(self._mapper.getEntity())
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
        
    def recalculateShares(self, community):
        totalArea = BigDecimal(0)
        for possession in community.getPossessions():
            totalArea = totalArea.add(possession.getArea())
        self._logger.info("Total area of community %s calculated as %f" % (community.getName(), totalArea.floatValue()))
        for possession in community.getPossessions():
            possessionArea = BigDecimal(possession.getArea().divide(totalArea).multiply(100.0))
            self._logger.info("Possession area for %d calculated as %f" % (possession.getId(), possessionArea))
            possession.setShare(possessionArea)
        