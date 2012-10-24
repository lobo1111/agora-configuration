class DictionaryManager(Container):
    
    _logger = Logger([:_scriptId])
    
    def getDictionaryType(self, typeName):
        sql = "Select dictType From DictionaryType dictType Where dictType.type = '%s'" % typeName
        _logger.info('Executing query: %s' % sql)
        return entityManager.createQuery(sql).getSingleResult();

    def findDictionaryInstance(self, typeName, key):
        sql = "Select dict From Dictionary dict Join dict.type dictType Where dictType.type = '%s' And dict.key = '%s'" % (typeName, key)
        _logger.info('Executing query: %s' % sql)
        return entityManager.createQuery(sql).getSingleResult();
    
    def getDictionaryInstance(self, id):
        sql = "Select dict From Dictionary dict Where dict.id = %s" % id
        _logger.info('Executing query: %s' % sql)
        return entityManager.createQuery(sql).getSingleResult();