from pl.reaper.container.data import Dictionary
from base.Container import Container

class ZpkDictionaryManager(Container):
    def create(self):
        entity = Dictionary()
        self.setData(entity)
        self.save(entity)
    
    def update(self):
        entity = self.findById(svars.get('id'))
        self.setData(entity)
        self.save(entity)
    
    def save(self, entity):
        entityManager.persist(entity)
    
    def setData(self, entity):
        entity.setType(self.findZpkDictType())
        entity.setKey(svars.get('dictKey'))
        entity.setValue(svars.get('dictValue'))
    
    def findById(self, id):
        return entityManager.createQuery("Select e From Dictionary e Where e.id = %s" % id).getSingleResult()
    
    def findZpkDictType(self):
        return entityManager.createQuery("Select e From DictionaryType e Where e.type = 'ZPKS'").getSingleResult()
