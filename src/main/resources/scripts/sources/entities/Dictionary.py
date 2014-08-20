from base.Container import Container

class DictionaryManager(Container):
    
    def getDictionaryType(self, typeName):
        sql = "Select dictType From DictionaryType dictType Where dictType.type = '%s'" % typeName
        self._logger.info('Executing query: %s' % sql)
        return self._entityManager.createQuery(sql).getSingleResult()

    def findDictionaryInstance(self, typeName, key):
        sql = "Select dict From Dictionary dict Join dict.type dictType Where dictType.type = '%s' And dict.key = '%s'" % (typeName, key)
        self._logger.info('Executing query: %s' % sql)
        return self._entityManager.createQuery(sql).getSingleResult()
    
    def getDictionaryInstance(self, id):
        sql = "Select dict From Dictionary dict Where dict.id = %s" % id
        self._logger.info('Executing query: %s' % sql)
        return self._entityManager.createQuery(sql).getSingleResult()

    def findByLabel(self, type, label):
        return self._entityManager.createQuery("Select d From Dictionary d Join d.type t Where t.type = '%s' Amd d.value = '%s'" % (type, label)).getSingleResult()