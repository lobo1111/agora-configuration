from pl.reaper.container.data import Community

class SyncAccessToDb(Container):
    def __init__(self):
        self.syncCommunities()
    
    def loadData(self, query):
        query = oldEntityManager.createQuery(query)
        return query.getResultList()
    
    
    def syncCommunities(self):
        communities = self.loadData('SELECT w FROM Wspolne w')
        for community in communities:
            if self.communityExists(community):
                self.communityUpdate(community)
            else:
                self.communityInsert(community)
                
    def communityExists(self, community):
        return syncDataExists('sync_community', 'erp_community_id', community.getId())
    
    def communityUpdate(self, oldCommunity):
        id = self.findBaseId('sync_community', 'erp_community_id', 'access_community_id', oldCommunity.getId())
        community = self.findCommunity(id)
        self.setDataAndPersistCommunity(oldCommunity, community)
        
    def findCommunity(self, id):
        return entityManager.createQuery(('SELECT c FROM Community c WHERE c.id = %d' % id)).getSingleResult()
    
    def findBaseId(self, tableName, baseIdColumnName, oldIdColumnName, oldId):
        return (entityManager.createNativeQuery(('SELECT %s FROM %s WHERE %s = %d' % (baseIdColumnName, tableName, oldIdColumnName, oldId))).getSingleResult())[0]
    
    def communityInsert(self, oldCommunity):
        community = Community()
        self.setDataAndPersistCommunity(oldCommunity, community)
        entityManager.createNativeQuery(('INSERT INTO sync_community(`erp_community_id`, `access_community_id`) VALUES(%d, %d)' % (community.getId(), oldCommunity.getId()))).executeUpdate()
        
    def setDataAndPersistCommunity(self, oldCommunity, community):
        community.setName(oldCommunity.getNazwa())
        community.setArea(float(oldCommunity.getPow()))
        community.setInDate(oldCommunity.getDataprz())
        community.setOutDate(oldCommunity.getDatawyl())
        entityManager.persist(community)
    
    def syncDataExists(self, tableName, idColumnName, id):
        try:
            entityManager.createNativeQuery(('SELECT * FROM %s WHERE %s = %s' % (tableName, idColumnName, id))).getSingleResult()
            return True
        except:
            return False