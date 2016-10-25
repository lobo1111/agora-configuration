from base.Container import Container
from java.io import StringWriter
from org.apache.velocity import VelocityContext
from org.apache.velocity.app import VelocityEngine

class StateTemplateGenerator(Container):
    
    def __init__(self):
        self._template = self.findBy("Template", "name", "'possession-account-state'")
        self._ve = VelocityEngine()
        self._ve.init()
        self._context = VelocityContext()
    
    def generateTemplate(self, stateRent, stateRF, chargingRent, chargingRT):
        self._context.put('stateRent', stateRent)
        self._context.put('stateRF', stateRF)
        self._context.put('chargingRent', chargingRent)
        self._context.put('chargingRT', chargingRT)
        writer = StringWriter()
        self._ve.evaluate(self._context, writer, self._template.getName(), unicode(self._template.getSource()))
        evaluatedTemplate = writer.toString()
        return evaluatedTemplate