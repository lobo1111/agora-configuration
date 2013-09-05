from pl.reaper.container.data import Community
from java.math import BigDecimal
from java.math import RoundingMode

class CommunityManager(Container):
    _logger = Logger([:_scriptId])
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix
        
    def create(self):
        community = Community()
        self.setCommunityData(community)
        self.setZpkData(community)
        self.saveCommunity(community)
        self.addDefaultElements(community)
        self.setObligationData(community)
        
    def update(self):
        community = self.findCommunity()
        self.setCommunityData(community)
        self.setZpkData(community)
        self.saveCommunity(community)
        self.setElementsData(community)
        
    def setCommunityData(self, community):
        community.setName(vars.get('name'))
        community.setCompany(self.getCompany(community))
        
    def setElementsData(self, community):
        for i in range(int(vars.get(self._prefix + 'elementsCount'))): 
            vars.put("elementId", vars.get(self._prefix + str(i) + "_elementId"))
            vars.put("override", vars.get(self._prefix + str(i) + "_override"))
            vars.put("overrideValue", vars.get(self._prefix + str(i) + "_overrideValue"))
            manager = ElementManager()
            manager.CreateOrUpdateCommunityElement(community)
            
    def addDefaultElements(self, community):
        manager = ElementManager()
        manager.addDefaultElements(community)
        
    def getCompany(self, community):
        companyManager = CompanyManager()
        return companyManager.getCompany(community)
        
    def saveCommunity(self, community):
        self._logger.info(community.longDescription())
        entityManager.persist(community)
        entityManager.flush()
        
    def setZpkData(self, community):
        for i in range(int(vars.get(self._prefix + 'zpkCount'))): 
            vars.put(self._prefix + str(i) + "_communityId", vars.get(self._prefix + 'id'))
            manager = ZpkManager()
            manager.setPrefix(self._prefix + str(i) + "_")
            zpk = manager.create()
            zpk.setCommunity(community)
            community.getZpks().add(zpk)

    def setObligationData(self, community):
        for i in range(int(vars.get(self._prefix + 'obligationsCount'))): 
            prefix = self._prefix + str(i)
            vars.put(prefix + 'communityId', str(community.getId()))
            obligationManager = ObligationManager()
            obligationManager.setPrefix(prefix)
            obligation = obligationManager.create()
            community.getZpks().add(obligation.getZpk())
            self.saveCommunity(community)
            
    def findCommunity(self):
        id = vars.get('id')
        return self.findCommunityById(id)

    def findCommunityById(self, id):
        try:
            return entityManager.createQuery('Select community From Community community Where community.id = ' + str(id)).getSingleResult()
        except:
            self._logger.error('Can\'t load community. Tried to load by id stored as ' + str(id))

    def recalculateShares(self, communityId):
        community = self.findCommunityById(communityId)
        area = 0
        for possession in community.getPossessions():
            area += possession.getArea().floatValue()
        self._logger.info('Area recalculated(%s) on community %s' % (str(area), community.getName()))
        community.setArea(BigDecimal(area))
        entityManager.persist(community)
        area = BigDecimal(area)
        for possession in community.getPossessions():
            if possession.getArea().floatValue() > 0:
                share = possession.getArea().divide(area, 10, RoundingMode.HALF_UP)
                possession.setShare(share.multiply(BigDecimal(100)).setScale(2, RoundingMode.HALF_UP))
            else:
                possession.setShare(BigDecimal(0))
            self._logger.info('Share recalculated(%s) on possession %s' % (str(possession.getShare().floatValue()), str(possession.getId())))
            entityManager.persist(possession)