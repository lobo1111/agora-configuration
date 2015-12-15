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
        
    def startTransaction(self):
        if self._transaction != None:
            self._transaction.rollback()
        self._transaction = self._entityManager.getTransaction(); 
        self._transaction.begin()
        
    def commitTransaction(self):
        if self._transaction != None:
            self._transaction.commit()
            self._transaction = None
        
    def cancelTransaction(self):
        print "Rolling back transaction due to:"
        print "Unexpected error:", sys.exc_info()[0]
        print "Unexpected error:", sys.exc_info()[1]
        print "Unexpected error:", sys.exc_info()[2]
        if self._transaction != None:
            self._transaction.rollback()
            self._transaction = None

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
        self._entityManager.persist(entity)
        self._entityManager.flush()
        if hasattr(entity, 'getId'):
            self._svars.put('output', str(entity.getId()))
        return entity
