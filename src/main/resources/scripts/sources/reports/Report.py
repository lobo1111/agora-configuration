from base.Container import Container
from java.io import StringWriter
from org.apache.velocity import VelocityContext
from org.apache.velocity.app import VelocityEngine
from java.text import SimpleDateFormat
from java.util import Date

class Report(Container):
    
    def getReport(self):
        self.initTemplate()
        self.obtainData()
        self.fillTemplate()
        self.additionalData()
        self._svars.put('output', self.generateReport())
        
    def additionalData(self):
        self._context.put("date", str(SimpleDateFormat('dd-MM-yyyy').format(Date())))
    
    def initTemplate(self):
        self._template = self.findBy("Template", "name", self.getTemplateName())
        self._ve = VelocityEngine()
        self._ve.init()
        self._context = VelocityContext()
        
    def generateReport(self):
        writer = StringWriter()
        self._ve.evaluate(self._context, writer, self._template.getName(), unicode(self._template.getSource()))
        evaluatedTemplate = writer.toString()
        return evaluatedTemplate