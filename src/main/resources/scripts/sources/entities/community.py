from pl.reaper.container.data import Community
from java.math import BigDecimal

class CommunityManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        community = Community()
        self.setCommunityData(community)
        self.saveCommunity(community)
        
    def update(self):
        community = self.findCommunity()
        self.setCommunityData(community)
        self.saveCommunity(community)
        
    def setCommunityData(self, community):
        community.setName(vars.get('name'))
        community.setCompany(self.getCompany(community))
        
    def getCompany(self, community):
        companyManager = CompanyManager()
        return companyManager.getCompany(community)
        
    def saveCommunity(self, community):
        self._logger.info(community.longDescription())
        entityManager.persist(community)
        entityManager.flush()

    def findCommunity(self):
        id = vars.get('id')
        return self.findCommunityById(id)

    def findCommunityById(self, id):
        return entityManager.createQuery('Select community From Community community Where community.id = ' + str(id)).getSingleResult()

    def recalculateShares(self, communityId):
        community = self.findCommunityById(communityId)
        area = 0
        for possession in community.getPossessions():
            area += possession.getArea().floatValue()
        community.setArea(BigDecimal(area))
        entityManager.persist(community)
        area = BigDecimal(area)
        for possession in community.getPossessions():
            share = area.divide(possession.getArea())
            possession.setShare(share.multiply(BigDecimal(100)))
            entityManager.persist(possession)