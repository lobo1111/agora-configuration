class DictionaryManager(Container):
    def getDictionaryType(self, typeName):
        sql = "Select dictType From DictionaryType dictType Where dictType.type = '%s'" % typeName
        return entityManager.createQuery(sql).getSingleResult();

    def findDictionaryInstance(self, typeName, key):
        sql = "Select dict From Dictionary dict Join dict.type dictType Where dictType.type = '%s' And dict.key = '%s'" % (typeName, key)
        return entityManager.createQuery(sql).getSingleResult();
    
    def getDictionaryInstance(self, id):
        sql = "Select dict From Dictionary dict Where dict.id = %s" % id
        return entityManager.createQuery(sql).getSingleResult();