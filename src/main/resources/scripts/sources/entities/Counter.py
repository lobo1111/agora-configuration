from pl.reaper.container.data import Counter
from base.Container import Container
from entities.Dictionary import DictionaryManager

class CounterManager(Container):
    
    def create(self):
        counter = Counter()
        self.setCounterData(counter)
        self.saveEntity(counter)
        
    def update(self):
        counter = self.findById('Counter', self._svars.get('id'))
        self.setCounterData(counter)
        self.saveEntity(counter)

    def setCounterData(self, counter):
        counter.setType(DictionaryManager().getDictionaryInstance(self._svars.get('groupId')))
        counter.setInstallation(self.parseDate(self._svars.get('installation')))
        counter.setDecomission(self.parseDate(self._svars.get('decomission')))
        counter.setSerialNumber(self._svars.get('serialNumber'))
        if not (self._svars.get('parentId') == ''):
            counter.setParent(self.findById('Counter', self._svars.get('parentId')))

