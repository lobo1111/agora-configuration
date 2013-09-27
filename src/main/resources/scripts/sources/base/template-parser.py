from java.io import StringWriter
from org.apache.velocity import VelocityContext
from org.apache.velocity.app import VelocityEngine

import sys

class TemplateParser(Container):
    _logger = Logger([:_scriptId])
    _single = False
    _insertLimit = False
    _update = False
    _native = False

    def find(self, name):
        try:
            query = 'SELECT t FROM Template t WHERE t.name = :name'
            query = entityManager.createQuery(query)
            query.setParameter('name', name)
            return query.getSingleResult()
        except:
            self._logger.info('Template %s not found !' % name)
            return None

    def evaluate(self, template):
        ve = VelocityEngine()
        ve.init()
        context = VelocityContext()
        for var in template.getTemplateVariableCollection():
            context.put(var.getName(), self.loadData(var.getData()))
        writer = StringWriter()
        ve.evaluate(context, writer, template.getName(), unicode(template.getSource()))
        evaluatedTemplate = writer.toString()
        return evaluatedTemplate

    def loadData(self, data):
        data = self.insertVariables(data)
        self._logger.info('Executing query [%s]' % data)
        query = None
        if self._native:
            query = entityManager.createNativeQuery(data)
            self._native = False
        else:
            query = entityManager.createQuery(data)
        if self._insertLimit:
            query = self.insertLimit(query)
            self._insertLimit = False
        if self._update:
            self._update = False
            return query.executeUpdate()
        else:
            if self._single:
                self._single = False
                try:
                    singleResult = query.getSingleResult()
                    self._logger.info('Single result found: %s' % str(singleResult))
                    return singleResult
                except:
                    self._logger.warn(sys.exc_info()[1])
                    return None
            else:
                return query.getResultList()

    
    def insertLimit(self, query):
        if vars.get('limit') != None:
            self._logger.info('Inserting limit %s' % vars.get('limit'))
            query.setMaxResults(int(vars.get('limit')))
        if vars.get('offset') != None:
            self._logger.info('Inserting offset %s' % vars.get('offset'))
            query.setFirstResult(int(vars.get('offset')))
        return query
    
    def insertVariables(self, data):
        r = l = -1
        while data.find("{:") != -1:
            l = data.find("{:")
            r = data.find("}")
            var = data[l : r + 1]
            if self.isSpecialVariable(var[2:-1]):
                data = self.handleSpecialVariable(data, var[2:-1])
            else:
                self._logger.info('Inserting variable %s=%s' % (var, vars.get(var[2:-1])))
                data = data.replace(var, (vars.get(var[2:-1])))
        return data
    
    def isSpecialVariable(self, variable):
        if variable in ['limit', 'single', 'update', 'native']:
            return True
        else:
            return False
        
    def handleSpecialVariable(self, data, variable):
        if variable == 'limit':
            self._logger.info('"insert limit" marker found')
            self._insertLimit = True
        elif variable == 'single':
            self._logger.info('"single" marker found')
            self._single = True
        elif variable == 'native':
            self._logger.info('"native" marker found')
            self._native = True
        elif variable == 'update':
            self._logger.info('"update" marker found')
            self._update = True
        data = data.replace('{:%s}' % variable, '')
        return data

    def __init__(self):
        self._templateName = vars.get('templateName')
    
    def parse(self):
        self._logger.info('Parsing template %s' % self._templateName)
        template = self.find(self._templateName)
        evaluated = self.evaluate(template)
        return evaluated
        