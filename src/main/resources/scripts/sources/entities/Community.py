from pl.reaper.container.data import Community
from java.math import BigDecimal
from java.math import RoundingMode
from base.Container import Container
from entities.Company import CompanyManager

class CommunityManager(Container):
    _prefix = ''
    
    def setPrefix(self, prefix):
        self._prefix = prefix
        
    def create(self):
        community = Community()
        self.setCommunityData(community)
        self.generateZpkNumber(community)
        self.saveCommunity(community)
        self.addDefaultElements(community)
        self.setContractorData(community)
        
    def update(self):
        community = self.findCommunity()
        self.setCommunityData(community)
        self.saveCommunity(community)
        self.setElementsData(community)
        
    def setCommunityData(self, community):
        global svars
        community.setName(svars.get('name'))
        community.setCompany(self.getCompany(community))
        if svars.get('hasDefaultAccount') == 'true':
            community.setDefaultAccount(self.findAccountById(svars.get('defaultAccountId')))
        else:
            community.setDefaultAccount(None)
        if svars.get('hasRepairFundAccount') == 'true':
            community.setRepairFundAccount(self.findAccountById(svars.get('repairFundAccountId')))
        else:
            community.setRepairFundAccount(None)

    def generateZpkNumber(self, community):
        manager = ZpkManager()
        zpkRent = manager.generateZpkForCommunity(community, "CHARGING_RENT")
        community.getZpks().add(zpkRent)
        zpkRepairFund = manager.generateZpkForCommunity(community, "CHARGING_REPAIR_FUND")
        community.getZpks().add(zpkRepairFund)
        
    def setElementsData(self, community):
        global svars
        for i in range(int(svars.get(self._prefix + 'elementsCount'))): 
            svars.put("elementId", svars.get(self._prefix + str(i) + "_elementId"))
            svars.put("override", svars.get(self._prefix + str(i) + "_override"))
            svars.put("overrideValue", svars.get(self._prefix + str(i) + "_overrideValue"))
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
        
    def setContractorData(self, community):
        global svars
        svars.put('communityId', str(community.getId()))
        svars.put('exsitingCompany', 'true')
        for company in self.findDefaultCompanies():
            svars.put('obligationCompanyId', str(company.getId()))
            obligationManager = ContractorManager()
            obligation = obligationManager.create()
            community.getZpks().addAll(obligation.getZpks())
        self.saveCommunity(community)
            
    def findCommunity(self):
        global svars
        id = svars.get('id')
        return self.findCommunityById(id)

    def findDefaultCompanies(self):
        return entityManager.createQuery('Select company From Company company Where company.defaultContractor = 1').getResultList()

    def findCommunityById(self, id):
        try:
            return entityManager.createQuery('Select community From Community community Where community.id = ' + str(id)).getSingleResult()
        except:
            self._logger.error('Can\'t load community. Tried to load by id stored as ' + str(id))

    def findAccountById(self, id):
        return entityManager.createQuery('Select a From Account a Where a.id = ' + str(id)).getSingleResult()

    def recalculateShares(self, communityId):
        community = self.findCommunityById(communityId)
        area = 0
        possessions = community.getPossessions()
        self._logger.info('Recalculating shares on community(%s), found %s possession(s)' % (community.getId(), possessions.size()))
        for possession in possessions:
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