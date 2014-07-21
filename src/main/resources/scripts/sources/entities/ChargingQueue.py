from pl.reaper.container.data import ChargingQueue
from pl.reaper.container.data.ChargingQueue import TYPE
from base.Container import Container

class ChargingQueueManager(Container):
        
    def addToQueue(self):
        cq = ChargingQueue()
        cq.setType(TYPE.ALL)
        self._entityManager.persist(cq)
    
    def popFromQueue(self):
        if self.itemsInQueue():
            item = self.getFirst()
            self._logger.info('item poped - %s' % str(item.getId()))
            self._entityManager.remove(item)
            self._entityManager.flush()
            return item
        else:
            self._logger.info('Charge queue is empty')
            return None
    
    def itemsInQueue(self):
        queueSize = self._entityManager.createQuery('Select count(cq.id) From ChargingQueue cq').getSingleResult()
        self._logger.info('charge queue size - %s' % str(queueSize))
        return queueSize
    
    def getFirst(self):
        return self._entityManager.createQuery('Select cq From ChargingQueue cq Order By cq.id ASC').getResultList()[0]
        