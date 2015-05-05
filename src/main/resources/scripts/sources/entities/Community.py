from pl.reaper.container.data import Community
from java.math import BigDecimal
from java.util import Date
from java.math import RoundingMode
from base.Container import Container
from entities.Account import AccountManager
from entities.Company import CompanyManager
from entities.Zpk import ZpkManager
from entities.Element import ElementManager
from entities.Contractor import ContractorManager
from entities.Dictionary import DictionaryManager

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
        self.addCounters(community)
        self.saveCommunity(community)
        
    def update(self):
        community = self.findCommunity()
        self.setCommunityData(community)
        self.saveCommunity(community)
        self.addElements(community)
        self.addContractors(community)
        self.addCounters(community)        
        self.saveCommunity(community)

    def decomission(self):
        community = self.findById("Community", self._svars.get('id'))
        community.setName("DECOMISSIONED + " + community.getName())
        community.setOutDate(Date())
        
    def setCommunityData(self, community):
        community.setCompany(self.getCompany(community))
        community.setName(community.getCompany().getName())
        repairFundAccountCleared = False
        repairFundAccountNoChanges = False
        if (self._svars.get('repairFundAccountNumber') != '' and (community.getRepairFundAccount() == None) or (community.getRepairFundAccount() != None and community.getRepairFundAccount().getNumber() != self._svars.get('repairFundAccountNumber'))):
            if self._svars.get('repairFundAccountNumber') == '':
                community.setRepairFundAccount(None)
                repairFundAccountCleared = True
                self._logger.info('Repair fund account cleared')
            else:
                self._svars.put('accountNumber', self._svars.get('repairFundAccountNumber'))
                self._svars.put('accountType', 'REPAIR_FUND')
                account = AccountManager().createNewAccount(community)
                community.setRepairFundAccount(account)
                if community.getDefaultAccount() != None:
                    community.getDefaultAccount().setType(DictionaryManager().findDictionaryInstance('ACCOUNT_TYPE', 'RENT'))
                    for zpk in community.getDefaultAccount().getZpks():
                        if zpk.getType().getKey() == 'REPAIR_FUND':
                            community.getDefaultAccount().getZpks().remove(zpk)
                            zpk.setAccount(None)
                self._logger.info('Repair fund account changed')
        else:
            self._logger.info('No changes to repair fund account has been done')
            repairFundAccountNoChanges = True
        if community.getDefaultAccount() == None or community.getDefaultAccount().getNumber() != self._svars.get('defaultAccountNumber'):
            self._svars.put('accountNumber', self._svars.get('defaultAccountNumber'))
            if community.getRepairFundAccount() == None:
                self._svars.put('accountType', 'DEFAULT')
            else:
                self._svars.put('accountType', 'RENT')
            account = AccountManager().createNewAccount(community)
            if community.getRepairFundAccount() == None and not repairFundAccountNoChanges:
                AccountManager().createRentZpk(account)
            community.setDefaultAccount(account)
            self._logger.info('Default account changed')
        else:
            if repairFundAccountCleared:
                account = community.getDefaultAccount()
                account.setType(DictionaryManager().findDictionaryInstance('ACCOUNT_TYPE', 'DEFAULT'))
                AccountManager().createRepairFundZpk(account)
                self._logger.info('Rent account has been transformed into default one')
            else:
                self._logger.info('No changes to default account has been done')

    def generateZpkNumber(self, community):
        manager = ZpkManager()
        manager.setEntityManager(self._entityManager)
        manager.setSvars(self._svars)
        zpkRent = manager.generateZpkForCommunity(community, "CHARGING_RENT")
        community.getZpks().add(zpkRent)
        zpkRepairFund = manager.generateZpkForCommunity(community, "CHARGING_REPAIR_FUND")
        community.getZpks().add(zpkRepairFund)
        
    def addElements(self, community):
        for i in range(int(self._svars.get(self._prefix + 'elementsCount'))): 
            self._svars.put("elementId", self._svars.get(self._prefix + str(i) + "_element_elementId"))
            self._svars.put("override", self._svars.get(self._prefix + str(i) + "_element_override"))
            self._svars.put("overrideValue", self._svars.get(self._prefix + str(i) + "_element_overrideValue"))
            communityElement = ElementManager().CreateOrUpdateCommunityElement(community)
            if self._svars.get(self._prefix + str(i) + "_element_remove") == 'true':
                ElementManager().dropCommunityElement(communityElement.getId())
            
    def getCompany(self, community):
        companyManager = CompanyManager()
        companyManager.setEntityManager(self._entityManager)
        companyManager.setSvars(self._svars)
        return companyManager.getCompany(community)
        
    def saveCommunity(self, community):
        self._logger.info(community.longDescription())
        self.saveEntity(community)
        
    def addContractors(self, community):
        contractorsManager = ContractorManager()
        for i in range(int(self._svars.get(self._prefix + 'contractorsCount'))): 
            self._svars.put(str(i) + 'communityId', str(community.getId()))
            contractorsManager.setPrefix(str(i))
            obligation = contractorsManager.create()
            community.getZpks().addAll(obligation.getZpks())
        self.saveCommunity(community)

    def addCounters(self, community):
        for i in range(int(self._svars.get(self._prefix + 'mainCountersCount'))): 
            counterId = self._svars.get(self._prefix + str(i) + '_counter_id')
            counter = self.findById('Counter', counterId)
            counter.setCommunity(community)
            community.getCounters().add(counter)
            self.saveCommunity(community)
            self._entityManager.persist(counter)

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

    def findByLabel(self, label):
        return self._entityManager.createQuery("Select d From Community d Join d.company c Where c.name = '%s'" % label).getSingleResult()
