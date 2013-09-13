from pl.reaper.container.data import ChargingQueue
from pl.reaper.container.data.ChargingQueue import TYPE

class ChargingQueue:
    def addToQueue(self):
        type = self.getType(vars.get('type'))
        communityId = vars.get('communityId')
        possessionId = vars.get('possessionId')
        cq = ChargingQueue()
        print dir(cq)
        if not communityId is None and communityId != '':
            cq.setCommunity(self.findCommunityById(communityId))
        if not possessionId is None and possessionId != '':
            cq.setPossession(self.findPossessionById(possessionId))
        cq.setType(type)
        entityManager.persist(cq)
    
    def popFromQueue(self):
        item = self.getFirst()
        entityManager.remove(item)
        return item
    
    def getType(self, type): 
        if type == "ALL":
            return TYPE.ALL
        elif type == "COMMUNITY":
            return TYPE.COMMUNITY
        elif type == "POSSESSION":
            return TYPE.POSSESSION
        return None
    
    def getFirst(self):
        try:
            return entityManager.createQuery('Select item From ChargingQueue cq Order By cq.id ASC').getSingleResult()
        except:
            return None
        
    def findCommunityById(self, id):
        return entityManager.createQuery('Select community From Community community Where community.id = ' + str(id)).getSingleResult()
    
    def findPossessionById(self, id):
        return entityManager.createQuery('Select possession From Possession possession Where possession.id = ' + str(id)).getSingleResult()
    