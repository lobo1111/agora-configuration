from pl.reaper.container.data import Community
from java.math import BigDecimal
from java.math import RoundingMode
from base.Container import Container
from entities.Account import AccountManager
from entities.Company import CompanyManager
from entities.Zpk import ZpkManager
from entities.Element import ElementManager
from entities.Contractor import ContractorManager

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
        self.addContractors(community)
        
    def update(self):
        community = self.findCommunity()
        self.setCommunityData(community)
        self.saveCommunity(community)
        self.setElementsData(community)
        
    def setCommunityData(self, community):
        community.setCompany(self.getCompany(community))
        community.setName(community.getCompany().getName())
        if self._svars.get('hasDefaultAccount') == 'true':
            account = self.findAccountById(self._svars.get('defaultAccountId'))
            acount.setCommunity(community)
            community.setDefaultAccount()
            AccountManager().createZpk(account)
        if self._svars.get('hasRepairFundAccount') == 'true':
            account = self.findAccountById(self._svars.get('repairFundAccountId'))
            acount.setCommunity(community)
            community.setRepairFundAccount()
            AccountManager().createZpk(account)

    def generateZpkNumber(self, community):
        manager = ZpkManager()
        manager.setEntityManager(self._entityManager)
        manager.setSvars(self._svars)
        zpkRent = manager.generateZpkForCommunity(community, "CHARGING_RENT")
        community.getZpks().add(zpkRent)
        zpkRepairFund = manager.generateZpkForCommunity(community, "CHARGING_REPAIR_FUND")
        community.getZpks().add(zpkRepairFund)
        
    def setElementsData(self, community):
        for i in range(int(self._svars.get(self._prefix + 'elementsCount'))): 
            self._svars.put("elementId", self._svars.get(self._prefix + str(i) + "_elementId"))
            self._svars.put("override", self._svars.get(self._prefix + str(i) + "_override"))
            self._svars.put("overrideValue", self._svars.get(self._prefix + str(i) + "_overrideValue"))
            manager = ElementManager()
            manager.setEntityManager(self._entityManager)
            manager.setSvars(self._svars)
            manager.CreateOrUpdateCommunityElement(community)
            
    def addDefaultElements(self, community):
        manager = ElementManager()
        manager.setEntityManager(self._entityManager)
        manager.setSvars(self._svars)
        manager.addDefaultElements(community)
        
    def getCompany(self, community):
        companyManager = CompanyManager()
        companyManager.setEntityManager(self._entityManager)
        companyManager.setSvars(self._svars)
        return companyManager.getCompany(community)
        
    def saveCommunity(self, community):
        self._logger.info(community.longDescription())
        self._entityManager.persist(community)
        self._entityManager.flush()
        
    def addContractors(self, community):
        self._svars.put('communityId', str(community.getId()))
        self._svars.put('exsitingCompany', 'true')
        for company in self.findDefaultCompanies():
            self._svars.put('obligationCompanyId', str(company.getId()))
            obligationManager = ContractorManager()
            obligationManager.setEntityManager(self._entityManager)
            obligationManager.setSvars(self._svars)
            obligation = obligationManager.create()
            community.getZpks().addAll(obligation.getZpks())
        self.saveCommunity(community)
            
    def findCommunity(self):
        id = self._svars.get('id')
        return self.findCommunityById(id)

    def findDefaultCompanies(self):
        return self._entityManager.createQuery('Select company From Company company Where company.defaultContractor = 1').getResultList()

    def findCommunityById(self, id):
        try:
            return self._entityManager.createQuery('Select community From Community community Where community.id = ' + str(id)).getSingleResult()
        except:
            self._logger.error('Can\'t load community. Tried to load by id stored as ' + str(id))

    def findAccountById(self, id):
        return self._entityManager.createQuery('Select a From Account a Where a.id = ' + str(id)).getSingleResult()

    def recalculateShares(self, communityId):
        community = self.findCommunityById(communityId)
        area = 0
        possessions = community.getPossessions()
        self._logger.info('Recalculating shares on community(%s), found %s possession(s)' % (community.getId(), possessions.size()))
        for possession in possessions:
            area += possession.getArea().floatValue()
        self._logger.info('Area recalculated(%s) on community %s' % (str(area), community.getName()))
        community.setArea(BigDecimal(area))
        self._entityManager.persist(community)
        area = BigDecimal(area)
        for possession in community.getPossessions():
            if possession.getArea().floatValue() > 0:
                share = possession.getArea().divide(area, 10, RoundingMode.HALF_UP)
                possession.setShare(share.multiply(BigDecimal(100)).setScale(2, RoundingMode.HALF_UP))
            else:
                possession.setShare(BigDecimal(0))
            self._logger.info('Share recalculated(%s) on possession %s' % (str(possession.getShare().floatValue()), str(possession.getId())))
            self._entityManager.persist(possession)