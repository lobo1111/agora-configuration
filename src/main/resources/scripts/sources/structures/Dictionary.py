from base.Container import Container

class DictionaryManager(Container):
    
    def findDictionaryInstance(self, typeName, key):
        sql = "Select dict From Dictionary dict Join dict.type dictType Where dictType.type = '%s' And dict.key = '%s'" % (typeName, key)
        return self._entityManager.createQuery(sql).getSingleResult()
    
    def findByValue(self, typeName, value):
        sql = "Select dict From Dictionary dict Join dict.type dictType Where dictType.type = '%s' And dict.value = '%s'" % (typeName, value)
        return self._entityManager.createQuery(sql).getSingleResult()