from pl.reaper.container.data import Dictionary

class ZpkDictionaryManager:
    def create(self):
        entity = Dictionary()
        self.setData(entity)
        self.save(entity)
    
    def update(self):
        entity = self.findById(vars.get('id'))
        self.setData(entity)
        self.save(entity)
    
    def save(self, entity):
        entityManager.persist(entity)
    
    def setData(self, entity):
        entity.setType(self.findZpkDictType())
        entity.setKey(vars.get('dictKey'))
        entity.setValue(vars.get('dictValue'))
    
    def findById(self, id):
        return entityManager.createQuery("Select e From Dictionary e Where e.id = %s" % id).getSingleResult()
    
    def findZpkDictType(self):
        return entityManager.createQuery("Select e From DictionaryType e Where e.type = 'ZPKS'").getSingleResult()
