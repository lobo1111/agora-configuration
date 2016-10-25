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
    
    def generateTemplate(self, calculator):
        self._logger.info(stateRent)
        self._context.put('stateRent', calculator.calculateCurrentRentState())
        self._context.put('stateRF', calculator.calculateCurrentRFState())
        self._context.put('chargingRent', calculator.calculateRentCharging())
        self._context.put('chargingRT', calculator.calculateRFCharging())
        writer = StringWriter()
        self._ve.evaluate(self._context, writer, self._template.getName(), unicode(self._template.getSource()))
        evaluatedTemplate = writer.toString()
        return evaluatedTemplate