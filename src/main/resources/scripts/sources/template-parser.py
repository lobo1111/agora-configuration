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
        return entityManager.createQuery(data).getResultList()

    def __init__(self):
        self._templateName = vars.get('templateName')
    
    def parse(self):
        template = self.find(self._templateName)
        evaluated = self.evaluate(template)
        output.setResult(evaluated)
        