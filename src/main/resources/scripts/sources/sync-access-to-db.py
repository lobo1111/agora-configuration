from pl.reaper.container.data.old import Wspolne

class SyncAccessToDb(Container):
    def __init__(self):
        self.syncCommunities()
    
    def loadData(self, query):
        query = oldEntityManager.createQuery(query)
        return query.getResultList()
    
    
    def syncCommunities(self):
        communities = self.loadData('SELECT w FROM Wspolne w')
        for community in communities:
            print community