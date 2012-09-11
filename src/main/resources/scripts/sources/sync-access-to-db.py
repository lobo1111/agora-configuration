from pl.reaper.container.data import Community
from java.text import SimpleDateFormat

class SyncAccessToDb(Container):
    _logger = Logger([:_scriptId])
    _processed = 0
    _inserted = 0
    _updated = 0
    
    def __init__(self):
        self.syncCommunities()
    
    def loadData(self, query):
        query = oldEntityManager.createQuery(query)
        return query.getResultList()
    
    def syncCommunities(self):
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
        self._logger('communities synchronized[processed:%d][inserted:%d][updated:%d]' % (self._processed, self._inserted, self._updated))
                
    def communityExists(self, community):
        return self.syncDataExists('sync_community', 'access_community_id', community.getId())
    
    def communityUpdate(self, oldCommunity):
        id = self.findBaseId('sync_community', 'erp_community_id', 'access_community_id', oldCommunity.getId())
        community = self.findCommunity(id)
        self.setDataAndPersistCommunity(oldCommunity, community)
        
    def findCommunity(self, id):
        return entityManager.createQuery(('SELECT c FROM Community c WHERE c.id = %d' % id)).getSingleResult()
    
    def findBaseId(self, tableName, baseIdColumnName, oldIdColumnName, oldId):
        sql = 'SELECT %s FROM %s WHERE %s = %d' % (baseIdColumnName, tableName, oldIdColumnName, oldId)
        return (entityManager.createNativeQuery(sql).getSingleResult())[0]
    
    def communityInsert(self, oldCommunity):
        community = Community()
        community = self.setDataAndPersistCommunity(oldCommunity, community)
        self._logger.info('new community bound: %d <-> %d' % (oldCommunity.getId(), community.getId()))
        entityManager.createNativeQuery('INSERT INTO sync_community(`erp_community_id`, `access_community_id`) VALUES(%d, %d)' % (community.getId(), oldCommunity.getId())).executeUpdate()
        
    def setDataAndPersistCommunity(self, oldCommunity, community):
        community.setName(oldCommunity.getNazwa())
        if oldCommunity.getPow() == 'None':
            oldCommunity.setPow(float('0'))
        community.setArea(float(oldCommunity.getPow()))
        community.setInDate(self.parseDate(oldCommunity.getDataprz()))
        if oldCommunity.getDatawyl() != 'None':
            community.setOutDate(self.parseDate(oldCommunity.getDatawyl()))
        entityManager.persist(community)
        entityManager.flush()
        return community
    
    def syncDataExists(self, tableName, idColumnName, id):
        try:
            entityManager.createNativeQuery(('SELECT * FROM %s WHERE %s = %s' % (tableName, idColumnName, id))).getSingleResult()
            return True
        except:
            return False
        
    def parseDate(self, dateToParse): #Wed Sep 01 00:00:00 GMT 2010
        return SimpleDateFormat('EEE MMM dd HH:mm:ss z yyyy').parse(dateToParse)