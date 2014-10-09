from pl.reaper.container.data import Counter
from base.Container import Container
from entities.Dictionary import DictionaryManager

class CounterManager(Container):
    
    def create(self):
        counter = Counter()
        self.setCounterData(counter)
        self.saveCounter(counter)
        
    def update(self):
        counter = self.findCounter()
        self.setCounterData(counter)
        self.saveCounter(counter)

    def setCounterData(self, counter):
        counter.setType(DictionaryManager().getDictionaryInstance(self._svars.get('groupId')))
        counter.setInstallation(self.parseDate(self._svars.get('installation')))
        counter.setDecomission(self.parseDate(self._svars.get('decomission')))
        counter.setCommunity(self.findCommunityById(self._svars.get('communityId')))
        counter.setPossession(self.findPossessionById(self._svars.get('possessionId')))
        counter.setCounter(self.findCounterById(self._svars.get('counterId')))

    def saveCounter(self, counter):
        self._entityManager.persist(counter)
        self._entityManager.flush()

    def findCounter(self):
        id = self._svars.get('id')
        return self.findCounterById(id)

    def findCounterById(self, id):
        return self._entityManager.createQuery('Select c From Counter c Where c.id = ' + str(id)).getSingleResult()

    def parseDate(self, dateAsString):
        try:
            return SimpleDateFormat('dd-MM-yy').parse(dateAsString)
        except:
            return None