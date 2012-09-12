from java.text import SimpleDateFormat

class Sync:
    def loadData(self, query):
        query = oldEntityManager.createQuery(query)
        return query.getResultList()
    
    def syncDataExists(self, tableName, idColumnName, id):
        try:
            entityManager.createNativeQuery(('SELECT * FROM %s WHERE %s = %s' % (tableName, idColumnName, id))).getSingleResult()
            return True
        except:
            return False

    def parseDate(self, dateToParse): #Wed Sep 01 00:00:00 GMT 2010
        return SimpleDateFormat('EEE MMM dd HH:mm:ss z yyyy').parse(dateToParse)
    
    def findStreet(self, oldId):
        result = self.findOldErp('Ulice', 'kul', oldId)
        return result.getNul()
    
    def findOldErp(self, tableName, field, value):
        sql = "SELECT q FROM %s q WHERE q.%s = '%s'" % (tableName, field, value)
        return oldEntityManager.createQuery(sql).getSingleResult()
    
    def findBaseId(self, tableName, baseIdColumnName, oldIdColumnName, oldId):
        sql = 'SELECT %s FROM %s WHERE %s = %d' % (baseIdColumnName, tableName, oldIdColumnName, oldId)
        return entityManager.createNativeQuery(sql).getSingleResult()
    
    def findCommunity(self, id):
        return entityManager.createQuery(('SELECT c FROM Community c WHERE c.id = %d' % id)).getSingleResult()
    
    def findPossession(self, id):
        return entityManager.createQuery(('SELECT c FROM Possession c WHERE c.id = %d' % id)).getSingleResult()