from base.Logger import Logger
import helpers
from java.text import SimpleDateFormat
import sys

class Container:
    _logger = Logger()
    
    def __init__(self):
        self._svars = helpers.svars
        self._entityManager = helpers.entityManager
        self._context = helpers.context
        
    def findBy(self, entityName, field, value):
        try:
            self._logger.info('Searching for %s/%s with value %s' % (entityName, field, value))
            sql = 'Select entity From %s entity where entity.%s = %s' % (entityName, field, value)
            self._logger.info(sql)
            result = self._entityManager.createQuery(sql).getSingleResult()
            self._logger.info('Entity found: %s' % str(result))
            return result
        except:
            self._logger.info('Entity not found %s/%s with value %s' % (entityName, field, value))
            self._logger.info("Error message: %s" % sys.exc_info()[0])
            self._logger.info("Error message: %s" % sys.exc_info()[1])
            return None
        
    def findAllBy(self, entityName, field, value):
        try:
            self._logger.info('Searching for %s/%s with value %s' % (entityName, field, value))
            sql = 'Select entity From %s entity where entity.%s = %s' % (entityName, field, value)
            self._logger.info(sql)
            result = self._entityManager.createQuery(sql).getResultList()
            self._logger.info('Entities found: %s' % str(result))
            return result
        except:
            self._logger.info('Entity not found %s/%s with value %s' % (entityName, field, value))
            self._logger.info("Error message: %s" % sys.exc_info()[0])
            self._logger.info("Error message: %s" % sys.exc_info()[1])
            return []

    def findById(self, entityName, id):
        return self.findBy(entityName, 'id', id)
    
    def setSvars(self, svars):
        self._svars = svars
        self._logger.setSvars(svars)
        
    def setEntityManager(self, entityManager):
        self._entityManager = entityManager
        self._logger.setEntityManager(entityManager)
        
    def parseDate(self, dateAsString):
        try:
            return SimpleDateFormat('dd-MM-yyyy').parse(dateAsString)
        except:
            return None

    def saveEntity(self, entity, putId=True):
        self._entityManager.persist(entity)
        self._entityManager.flush()
        if hasattr(entity, 'getId') and putId:
            self._svars.put('output', str(entity.getId()))
        return entity
    
    def removeEntity(self, entity):
        self._entityManager.remove(entity)
    
    def setError(self, error):
        self._logger.info(error)
        self._svars.put('output', str(error))
        
    def parseFloat(self, string):
        try:
            return float(string.replace(",", "."))
        except ValueError:
            return 0

    