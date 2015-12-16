import helpers
import traceback
from base.Logger import Logger
from java.text import SimpleDateFormat
import sys

class Container:
    _logger = Logger()
    
    def __init__(self):
        self._svars = helpers.svars
        self._entityManager = helpers.entityManager
        self._properties = helpers.properties
        self._context = helpers.context
        
    def startTransaction(self):
        self._transaction = self._context.getUserTransaction()
        self._transaction.begin()
        
    def commitTransaction(self):
        self._transaction.commit()
        
    def rollbackTransaction(self):
        self._logger.info("Error message: %s" % sys.exc_info()[0])
        self._logger.info("Error message: %s" % sys.exc_info()[1])
        self._transaction.rollback()
        
    def getParameter(self, name):
        value = self._svars.get(name)
        if value == None:
            self._logger.info("Param '%s' not set, assuming None" % name)
            return None
        else:
            self._logger.info("Getting parameter '%s' from session" % name)
            return value
        
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
        return self.findBy(entityName, 'id', id)
    
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

    def saveEntity(self, entity):
        self.startTransaction()
        self._entityManager.persist(entity)
        self.commitTransaction()
        if hasattr(entity, 'getId'):
            self._svars.put('output', str(entity.getId()))
        return entity
    
    def saveAtomic(self, entity, putId = False):
        try:
            self.startTransaction()
            self._entityManager.persist(entity)
            self.commitTransaction()
            if hasattr(entity, 'getId') and putId:
                self._svars.put('output', str(entity.getId()))
        except:
            self.rollbackTransaction()
        return entity