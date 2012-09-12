from java.text import SimpleDateFormat
from pl.reaper.container.data import Address
from pl.reaper.container.data import Company
from pl.reaper.container.data import Person
from pl.reaper.container.data import Possession
from pl.reaper.container.data import Owner
from java.math import BigDecimal

class SyncPossessions(Sync):
    _logger = Logger([:_scriptId])
    _processed = 0
    _inserted = 0
    _updated = 0
    
    def sync(self):
        self._logger.info('synchronizing possessiona')
        possessions = self.loadData('SELECT w FROM Mieszkania w')
        for possession in possessions:
            self._processed += 1
            self._logger.info('processing possession %s' % possession.getMieszkanie())
            if self.possessionExists(possession):
                self._logger.info('possession exists, updating')
                self.possessionUpdate(possession)
                self._updated += 1
            else:
                self._logger.info('possession doesn\'t exists, inserting')
                self.possessionInsert(possession)
                self._inserted += 1
        self._logger.info('possession synchronized[processed:%d][inserted:%d][updated:%d]' % (self._processed, self._inserted, self._updated))

    def possessionExists(self, possession):
        return self.syncDataExists('sync_possession', 'access_possession_id', possession.getId())
    
    def possessionUpdate(self, oldPossession):
        id = self.findBaseId('sync_possession', 'erp_possession_id', 'access_possession_id', oldPossession.getId())
        possession = self.findPossession(id)
        self.setDataAndPersistCommunity(oldPossession, possession)
    
    def possessionInsert(self, oldPossession):
        possession = Possession()
        self.setDataAndPersistCommunity(oldPossession, possession)
        self._logger.info('new possession bound: %d <-> %d' % (oldPossession.getId(), possession.getId()))
        entityManager.createNativeQuery('INSERT INTO sync_possession(`erp_possession_id`, `access_possession_id`) VALUES(%d, %d)' % (possession.getId(), oldPossession.getId())).executeUpdate()
        
    def setDataAndPersistCommunity(self, oldPossession, possession):
        self.setCommunity(oldPossession, possession)
        self.setAddress(oldPossession, possession)
        self.setOwner(oldPossession, possession)
        self.setPossession(oldPossession, possession)
        
    def setOwner(self, oldPossession, possession):
        pass
        
    def setPossession(self, oldPossession, possession):
        possession.setArea(oldPossession.getPow())
        possession.setShare(oldPossession.getUdzial())
        entityManager.persist(possession)
        
    def setAddress(self, oldPossession, possession):
        address = None
        if possession.getAddress() != None:
            address = possession.getAddress()
        else:
            address = Address()
        address.setStreet(self.findStreet(oldPossession.getKul()))
        address.setHouseNumber(oldPossession.getNrbr())
        address.setFlatNumber(oldPossession.getNrmie())
        address.setCity('Swidnica')
        entityManager.persist(address)
        possession.setAddress(address)
        
    def setCommunity(self, oldPossession, possession):
        oldCommunityId = (self.findOldErp('Wspolne', 'nrwsp', oldPossession.getNrwsp())).getId()
        communityId = self.findBaseId('sync_community', 'erp_community_id', 'access_community_id', oldCommunityId)
        community = self.findCommunity(communityId)
        possession.setCommunity(community)
        