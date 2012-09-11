class SyncAccessToDb(Container):
    def __init__(self):
        pass
    
    def loadData(self, query):
        query = oldEntityManager.createQuery(query)
        return query.getResultList()
    
    
    def syncCommunities(self):
        communities = self.loadData('SELECT * FROM wspolne')
        for community in communities:
            print community