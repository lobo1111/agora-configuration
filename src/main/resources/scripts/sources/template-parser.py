from java.io import StringWriter
from org.apache.velocity import VelocityContext
from org.apache.velocity.app import VelocityEngine

class TemplateParser(Container):

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
        data = self.insertVariables(self, data)
        query = entityManager.createQuery(data)
        query = self.insertLimit(self, query)
        return query.getResultList()
    
    def insertLimit(self, query):
        if vars.get('limit') != None:
            query.setMaxResults(int(vars.get('limit')))
        if vars.get('offset') != None:
            query.setFirstResult(int(vars.get('offset')))
        return query
    
    def insertVariables(self, data):
        r = l = -1
        while data.find("[:") != -1:
            l = data.find("[:")
            r = data.find("]")
            var = data[l : r + 1]
            data = data.replace(var, vars.get(var[2:-1]))
        return data

    def __init__(self):
        self._templateName = vars.get('templateName')
    
    def parse(self):
        template = self.find(self._templateName)
        evaluated = self.evaluate(template)
        output.setResult(evaluated)
        