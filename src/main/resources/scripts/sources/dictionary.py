class DictionaryManager(Container):
    def getDictionaryType(self, typeName):
        sql = "Select dictType From DictionaryType dictType Where dictType.type = %s" % typeName
        return entityManager.createQuery(sql).getSingleResult();

    def getDictionaryInstance(self, typeName, key):
        sql = "Select dict From Dictionary dict Join dict.type dictType Where dictType = %s And dict.key = %s" % (typeName, key)
        return entityManager.createQuery(sql).getSingleResult();