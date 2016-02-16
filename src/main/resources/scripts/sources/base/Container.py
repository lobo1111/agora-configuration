import helpers
from base.Logger import Logger
from java.text import SimpleDateFormat
from java.lang import Class
import sys

class Container:
    _logger = Logger()
    
    def __init__(self):
        self._svars = helpers.svars
        self._entityManager = helpers.entityManager
        self._properties = helpers.properties
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

    def findById(self, entityName, id):
        return self._entityManager.find(Class.forName("pl.reaper.container.data." + entityName), int(id))
    
    def setSvars(self, svars):
        self._svars = svars
        self._logger.setSvars(svars)
        
    def setEntityManager(self, entityManager):
        self._entityManager = entityManager
        self._logger.setEntityManager(entityManager)
        
    def setProperties(self, properties):
        self._properties = properties

    def parseDate(self, dateAsString):
        try:
            return SimpleDateFormat('dd-MM-yyyy').parse(dateAsString)
        except:
            return None

    def saveEntity(self, entity, putId = True):
        self._entityManager.persist(entity)
        self._entityManager.flush()
        if hasattr(entity, 'getId') and putId:
            self._svars.put('output', str(entity.getId()))
        return entity
    