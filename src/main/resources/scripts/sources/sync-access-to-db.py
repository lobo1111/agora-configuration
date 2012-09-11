class SyncAccessToDb(Container):
    def __init__(self):
        self.syncCommunities()
    
    def loadData(self, query):
        query = oldEntityManager.createNativeQuery(query)
        return query.getResultList()
    
    
    def syncCommunities(self):
        communities = self.loadData('SELECT * FROM wspolne')
        for community in communities:
            print community