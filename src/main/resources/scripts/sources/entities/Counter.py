from pl.reaper.container.data import Counter
from pl.reaper.container.data import CounterStatus
from base.Container import Container
from entities.Dictionary import DictionaryManager
from java.util import Date

class CounterManager(Container):
    
    def create(self):
        counter = Counter()
        self.setCounterData(counter)
        self.saveEntity(counter)
        
    def update(self):
        counter = self.findById('Counter', self._svars.get('id'))
        self.setCounterData(counter)
        self.addStatuses(counter)
        self.saveEntity(counter)

    def setCounterData(self, counter):
        if self._svars.get('type') == 'MAIN':
            counter.setType(DictionaryManager().getDictionaryInstance(self._svars.get('groupId')))
        elif self._svars.get('type') == 'POSSESSION':
            parent = self.findById('Counter', self._svars.get('parentId'))
            counter.setParent(parent)
            counter.setType(parent.getType())
        elif self._svars.get('type') == 'REPLACEMENT':
            oldCounter = self.findById('Counter', self._svars.get('replacementId'))
            counter.setReplacementOf(oldCounter)
            counter.setType(oldCounter.getType())
            counter.setParent(oldCounter.getParent())
        counter.setInstallation(self.parseDate(self._svars.get('installation')))
        counter.setDecomission(self.parseDate(self._svars.get('decomission')))
        counter.setSerialNumber(self._svars.get('serialNumber'))

    def addStatuses(self, counter):
        for i in range(int(self._svars.get('statusCount'))): 
            cStatus = CounterStatus()
            counter.getStatuses().add(cStatus)
            cStatus.setCounter(counter)
            cStatus.setStatus(float(self._svars.get('status_' + str(i))))
            cStatus.setTimestamp(Date())
            self._entityManager.persist(cStatus)

