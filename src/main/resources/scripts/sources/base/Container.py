import helpers
import traceback
from base.Logger import Logger
from java.text import SimpleDateFormat

class Container:
    _logger = Logger()
    
    def __init__(self):
        self._svars = helpers.svars
        self._entityManager = helpers.entityManager
        self._properties = helpers.properties

    def findById(self, entityName, id):
        try:
            sql = 'Select entity From %s entity where entity.id = %s' % (entityName, id)
            return self._entityManager.createQuery(sql).getSingleResult()
        except:
            return None
    
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
            return SimpleDateFormat('dd-MM-yy').parse(dateAsString)
        except:
            self._logger.error('Wrong date format "%s"' % dateAsString)
            self._logger.error(traceback.format_exc())
            return None

    def saveEntity(self, entity):
        self._entityManager.persist(entity)
        self._entityManager.flush()
