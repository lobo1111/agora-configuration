from pl.reaper.container.data import Community
from pl.reaper.container.data import Address
from pl.reaper.container.data import Company
from java.math import BigDecimal

class SyncCommunities(Sync):
    _logger = Logger([:_scriptId])
    _processed = 0
    _inserted = 0
    _updated = 0
    
    def sync(self):
        self._logger.info('synchronizing communities')
        communities = self.loadData('SELECT w FROM Wspolne w')
        for community in communities:
            self._processed += 1
            self._logger.info('processing community %s' % community.getNazwa())
            if self.communityExists(community):
                self._logger.info('community exists, updating')
                self.communityUpdate(community)
                self._updated += 1
            else:
                self._logger.info('community doesn\'t exists, inserting')
                self.communityInsert(community)
                self._inserted += 1
        self._logger.info('communities synchronized[processed:%d][inserted:%d][updated:%d]' % (self._processed, self._inserted, self._updated))
                
    def communityExists(self, community):
        return self.syncDataExists('sync_community', 'access_community_id', community.getId())
    
    def communityUpdate(self, oldCommunity):
        id = self.findBaseId('sync_community', 'erp_community_id', 'access_community_id', oldCommunity.getId())
        community = self.find('Community', id)
        self.setDataAndPersistCommunity(oldCommunity, community)
        
    def communityInsert(self, oldCommunity):
        community = Community()
        self.setDataAndPersistCommunity(oldCommunity, community)
        self._logger.info('new community bound: %d <-> %d' % (oldCommunity.getId(), community.getId()))
        entityManager.createNativeQuery('INSERT INTO sync_community(`erp_community_id`, `access_community_id`) VALUES(%d, %d)' % (community.getId(), oldCommunity.getId())).executeUpdate()
        
    def setDataAndPersistCommunity(self, oldCommunity, community):
        company = self.getCommunityCompany(community, oldCommunity)
        community = self.getCommunity(oldCommunity, community)
        community.setCompany(company)
        entityManager.persist(community)
        entityManager.flush()
        
    def getCommunity(self, oldCommunity, community):
        community.setName(oldCommunity.getNazwa())
        if oldCommunity.getPow() == 'None':
            oldCommunity.setPow('0.0')
        community.setArea(BigDecimal(oldCommunity.getPow()))
        community.setInDate(self.parseDate(oldCommunity.getDataprz()))
        if oldCommunity.getDatawyl() != 'None':
            community.setOutDate(self.parseDate(oldCommunity.getDatawyl()))
        return community
    
    def getCommunityCompany(self, community, oldCommunity):
        company = None
        if community.getCompany() == None:
            company = Company()
        else:
            company = community.getCompany()
        company.setNip(oldCommunity.getNip())
        company.setRegon(oldCommunity.getRegon())
        company.setName(oldCommunity.getNazwa())
        company.setAddress(self.getCommunityAddress(company, oldCommunity))
        entityManager.persist(company)
        return company
    
    def getCommunityAddress(self, company, oldCommunity):
        address = None
        if company.getAddress() == None:
            address = Address()
        else:
            address = company.getAddress()
        address.setStreet(self.findStreet(oldCommunity.getUlica()))
        address.setHouseNumber(oldCommunity.getNrbr())
        address.setPostalCode(oldCommunity.getKod())
        address.setCity('Swidnica')
        entityManager.persist(address)
        return address
    
