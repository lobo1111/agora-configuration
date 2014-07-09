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
        self.addElements(community)
        self.addContractors(community)
        self.saveCommunity(community)
        
    def update(self):
        community = self.findCommunity()
        self.setCommunityData(community)
        self.saveCommunity(community)
        self.addElements(community)
        self.addContractors(community)
        self.saveCommunity(community)
        
    def setCommunityData(self, community):
        community.setCompany(self.getCompany(community))
        community.setName(community.getCompany().getName())
        if self._svars.get('hasDefaultAccount') == 'true' and (community.getDefaultAccount() == None or self._svars.get('defaultAccountId') != str(community.getDefaultAccount().getId())):
            account = self.findAccountById(self._svars.get('defaultAccountId'))
            account.setCommunity(community)
            community.setDefaultAccount(account)
            AccountManager().createZpk(account)
        if self._svars.get('hasRepairFundAccount') == 'true' and (community.getRepairFundAccount() == None or self._svars.get('repairFundAccountId') != str(community.getRepairFundAccount().getId())):
            account = self.findAccountById(self._svars.get('repairFundAccountId'))
            account.setCommunity(community)
            community.setRepairFundAccount(account)
            AccountManager().createZpk(account)

    def generateZpkNumber(self, community):
        manager = ZpkManager()
        manager.setEntityManager(self._entityManager)
        manager.setSvars(self._svars)
        zpkRent = manager.generateZpkForCommunity(community, "CHARGING_RENT")
        community.getZpks().add(zpkRent)
        zpkRepairFund = manager.generateZpkForCommunity(community, "CHARGING_REPAIR_FUND")
        community.getZpks().add(zpkRepairFund)
        
    def addElements(self, community):
        notToRemove = []
        for i in range(int(self._svars.get(self._prefix + 'elementsCount'))): 
            self._svars.put("elementId", self._svars.get(self._prefix + str(i) + "_elementId"))
            self._svars.put("override", self._svars.get(self._prefix + str(i) + "_override"))
            self._svars.put("overrideValue", self._svars.get(self._prefix + str(i) + "_overrideValue"))
            communityElement = ElementManager().CreateOrUpdateCommunityElement(community)
            notToRemove.append(communityElement.getId())
            self._logger.info('Element marked as not to remove: ' + str(communityElement.getId()))
        self._logger.info('Community has total elements: ' + str(community.getElements().size()))
        for element in community.getElements():
            self._logger.info('Checking if element should be dropped: ' + str(element.getId()))
            if not (element.getId() in notToRemove):
                self._logger.info('Element will be removed: ' + str(element.getId()))
                community.getElements().remove(element)
                self._entityManager.remove(element)
            else:
                self._logger.info('Element won\'t be removed: ' + str(element.getId()))
        self._entityManager.persist(community)        
            
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
        contractorsManager = ContractorManager()
        for i in range(int(self._svars.get(self._prefix + 'contractorsCount'))): 
            self._svars.put(str(i) + 'communityId', str(community.getId()))
            contractorsManager.setPrefix(str(i))
            obligation = contractorsManager.create()
            community.getZpks().addAll(obligation.getZpks())
        self.saveCommunity(community)

    def findCommunity(self):
        id = self._svars.get('id')
        return self.findCommunityById(id)

    def findCommunityElements(self, id):
        return self._entityManager.createQuery('Select e From ElementCommunity e Where e.community.id = %d' % id).getResultList()

    def findCommunityContractors(self, id):
        return self._entityManager.createQuery('Select e From Contractor e Where e.community.id = %d' % id).getResultList()

    def findCommunityById(self, id):
        return self._entityManager.createQuery('Select community From Community community Where community.id = ' + str(id)).getSingleResult()

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