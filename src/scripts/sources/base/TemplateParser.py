from java.io import StringWriter
from org.apache.velocity import VelocityContext
from org.apache.velocity.app import VelocityEngine
from base.Container import Container
from java.text import SimpleDateFormat
from helpers.Label import LabelManager

import sys

class TemplateParser(Container):
    _single = False
    _insertLimit = False
    _update = False
    _native = False

    def find(self, name):
        try:
            query = 'SELECT t FROM Template t WHERE t.name = :name'
            query = self._entityManager.createQuery(query)
            query.setParameter('name', name)
            return query.getSingleResult()
        except:
            self._logger.info('Template %s not found !' % name)
            return None

    def evaluate(self, template):
        ve = VelocityEngine()
        ve.init()
        context = VelocityContext()
        context.put('_formatter', SimpleDateFormat("dd-MM-yyyy"))
        self._logger.info('Date formatter stored as _formatter')
        context.put('_label', LabelManager())
        self._logger.info('Label manager stored as _label')
        self._logger.info('Template contains %d variables' % len(template.getTemplateVariableCollection()))
        for var in template.getTemplateVariableCollection():
            self._logger.info('Preparing variable %s' % var.getName())
            context.put(var.getName(), self.loadData(var.getData()))
            self._logger.info('Variable %s stored' % var.getName())
        writer = StringWriter()
        ve.evaluate(context, writer, template.getName(), unicode(template.getSource()))
        evaluatedTemplate = writer.toString()
        return evaluatedTemplate

    def loadData(self, data):
        data = self.insertVariables(data)
        self._logger.info('Executing query [%s]' % data)
        query = None
        if self._native:
            query = self._entityManager.createNativeQuery(data)
            self._native = False
        else:
            query = self._entityManager.createQuery(data)
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
                    self._logger.info(sys.exc_info()[1])
                    return None
            else:
                return query.getResultList()

    
    def insertLimit(self, query):
        
        if self._svars.get('limit') != None:
            self._logger.info('Inserting limit %s' % self._svars.get('limit'))
            query.setMaxResults(int(self._svars.get('limit')))
        if self._svars.get('offset') != None:
            self._logger.info('Inserting offset %s' % self._svars.get('offset'))
            query.setFirstResult(int(self._svars.get('offset')))
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
                self._logger.info('Inserting variable %s=%s' % (var, self._svars.get(var[2:-1])))
                data = data.replace(var, (self._svars.get(var[2:-1])))
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

    def parse(self):
        self._templateName = self._svars.get('templateName')
        self._logger.info('Parsing template %s' % self._templateName)
        template = self.find(self._templateName)
        evaluated = self.evaluate(template)
        return evaluated
        