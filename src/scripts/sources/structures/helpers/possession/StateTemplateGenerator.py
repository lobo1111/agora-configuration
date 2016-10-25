from base.Container import Container
from java.io import StringWriter
from org.apache.velocity import VelocityContext
from org.apache.velocity.app import VelocityEngine

class StateTemplateGenerator(Container):
    
    def generateTemplate(self, calculator):
        self._template = self.findBy("Template", "name", "'possession-account-state'")
        self._context = VelocityContext()
        self._context.put('stateRent', calculator.calculateCurrentRentState())
        self._context.put('stateRF', calculator.calculateCurrentRFState())
        self._context.put('chargingRent', calculator.calculateRentCharging())
        self._context.put('chargingRT', calculator.calculateRFCharging())
        writer = StringWriter()
        self._ve = VelocityEngine()
        self._ve.init()
        self._ve.evaluate(self._context, writer, self._template.getName(), unicode(self._template.getSource()))
        evaluatedTemplate = writer.toString()
        self._svars.put('output', evaluatedTemplate)