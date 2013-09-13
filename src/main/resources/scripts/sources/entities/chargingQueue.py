from pl.reaper.container.data import ChargingQueue
from pl.reaper.container.data.ChargingQueue import TYPE

class ChargingQueueManager:
    _logger = Logger([:_scriptId])
    def addToQueue(self):
        type = self.getType(vars.get('type'))
        communityId = vars.get('communityId')
        possessionId = vars.get('possessionId')
        cq = ChargingQueue()
        if not communityId is None and communityId != '0':
            cq.setCommunity(self.findCommunityById(communityId))
        if not possessionId is None and possessionId != '0':
            cq.setPossession(self.findPossessionById(possessionId))
        cq.setType(type)
        entityManager.persist(cq)
    
    def popFromQueue(self):
        item = self.getFirst()
        if not item is None:
            self._logger.info('item poped - %s' % str(item.getId()))
            entityManager.remove(item)
            entityManager.flush()
            return item
        else:
            self._logger.info('Charge queue is empty')
            return None
    
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
    