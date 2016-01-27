from base.Container import Container

class DictionaryManager(Container):
    
    def findDictionaryInstance(self, typeName, key):
        sql = "Select dict From Dictionary dict Join dict.type dictType Where dictType.type = '%s' And dict.key = '%s'" % (typeName, key)
        return self._entityManager.createQuery(sql).getSingleResult()