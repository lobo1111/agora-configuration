from pl.reaper.container.data import Address
from pl.reaper.container.data import Company
from pl.reaper.container.data import Person
from pl.reaper.container.data import Possession
from java.math import BigDecimal
from java.util import ArrayList

class SyncPossessions(Sync):
    _logger = Logger([:_scriptId])
    _processed = 0
    _inserted = 0
    _updated = 0
    
    def sync(self):
        self._logger.info('synchronizing possessions')
        possessions = self.loadData('SELECT w FROM Mieszkania w')
        for possession in possessions:
            self._processed += 1
#            self._logger.info('processing possession %s' % possession.getMieszkanie())
            if self.possessionExists(possession):
#                self._logger.info('possession exists, updating')
                self.possessionUpdate(possession)
                self._updated += 1
            else:
#                self._logger.info('possession doesn\'t exists, inserting')
                self.possessionInsert(possession)
                self._inserted += 1
        self._logger.info('possession synchronized[processed:%d][inserted:%d][updated:%d]' % (self._processed, self._inserted, self._updated))

    def possessionExists(self, possession):
        return self.syncDataExists('sync_possession', 'access_possession_id', possession.getId())
    
    def possessionUpdate(self, oldPossession):
        id = self.findBaseId('sync_possession', 'erp_possession_id', 'access_possession_id', oldPossession.getId())
        possession = self.find('Possession', id)
        self.setDataAndPersistPossession(oldPossession, possession)
    
    def possessionInsert(self, oldPossession):
        possession = Possession()
        self.setDataAndPersistPossession(oldPossession, possession)
        self._logger.info('new possession bound: %d <-> %d' % (oldPossession.getId(), possession.getId()))
        entityManager.createNativeQuery('INSERT INTO sync_possession(`erp_possession_id`, `access_possession_id`) VALUES(%d, %d)' % (possession.getId(), oldPossession.getId())).executeUpdate()
        
    def setDataAndPersistPossession(self, oldPossession, possession):
        self.setCommunity(oldPossession, possession)
        self.setAddress(oldPossession, possession)
        self.setOwner(oldPossession, possession)
        self.setPossession(oldPossession, possession)
        entityManager.flush()
        
    def setOwner(self, oldPossession, possession):
        owner = self.findOwner(oldPossession.getPlatnik())
        if owner.getPossessions() == None:
            owner.setPossessions(ArrayList())
        owner.getPossessions().clear()
        owner.getPossessions().add(possession)
        entityManager.persis(owner)
        
    def findOwner(self, platnikId):
        platnikId = oldPossession.getPlatnik()
        platnik = self.findOldErp('Platnicy', 'platnik', platnikId)
        id = self.findBaseId('sync_person', 'erp_person_id', 'access_person_id', platnik.getId())
        try:
            return self.find('Person', id)
        except:
            return self.find('Company', id)
        
    def setPossession(self, oldPossession, possession):
        if oldPossession.getPow() == 'None':
            oldPossession.setPow('0.0')
        possession.setArea(BigDecimal(oldPossession.getPow()))
        if oldPossession.getUdzial() == 'None':
            oldPossession.setUdzial('0.0')
        possession.setShare(BigDecimal(oldPossession.getUdzial()))
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
        community = self.find('Community', communityId)
        possession.setCommunity(community)
        