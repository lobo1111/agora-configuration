from java.io import StringWriter
from org.apache.velocity import VelocityContext
from org.apache.velocity.app import VelocityEngine

class TemplateParser(Container):
    _logger = Logger([:_scriptId])

    def find(self, name):
        query = 'SELECT t FROM Template t WHERE t.name = :name'
        query = entityManager.createQuery(query)
        query.setParameter('name', name)
        return query.getSingleResult()

    def evaluate(self, template):
        ve = VelocityEngine()
        ve.init()
        context = VelocityContext()
        for var in template.getTemplateVariableCollection():
            context.put(var.getName(), self.loadData(var.getData()))
        writer = StringWriter()
        ve.evaluate(context, writer, template.getName(), template.getSource())
        evaluatedTemplate = writer.toString()
        return evaluatedTemplate

    def loadData(self, data):
        data = self.insertVariables(data)
        self._logger.info('Executing query [%s]' % data)
        query = entityManager.createQuery(data)
        if self._insertLimit:
            query = self.insertLimit(query)
            self._insertLimit = False
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
                data = data.replace(var, vars.get(var[2:-1]))
        return data
    
    def isSpecialVariable(self, variable):
        if variable == 'limit':
            return True
        else:
            return False
        
    def handleSpecialVariable(self, data, variable):
        if variable == 'limit':
            self._insertLimit = True
            data = data.replace('[:%s]' % variable, '')
            return data

    def __init__(self):
        self._templateName = vars.get('templateName')
    
    def parse(self):
        template = self.find(self._templateName)
        evaluated = self.evaluate(template)
        output.setResult(evaluated)
        