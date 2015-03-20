from base.Container import Container
from crons.Charger import Calculator
from pl.reaper.container.data import ChargingElement
from java.io import StringWriter
from org.apache.velocity import VelocityContext
from org.apache.velocity.app import VelocityEngine

class ChargingReport(Container):

    def create(self):
        possession = self.findById("Possession", self._svars.get("id"))
        template = self.findBy("Template", "name", "charging-report")
        calculatedElements = self.calculateElements(possession)
        return self.compileTemplate(template, possession, calculatedElements)

    def calculateElements(self, possession):
        calculatedElements = []
        for element in possession.getElements():
            calculator = Calculator()
            cElement = ChargingElement()
            cElement.setName(element.getElement().getName())
            cElement.setGroup(element.getElement().getGroup())
            cElement.setValue(calculator.calculate(element, possession))
            calculatedElements.add(cElement)
        return calculatedElements

    def compileTemplate(template, possession, calculatedElements):
        ve = VelocityEngine()
        ve.init()
        context = VelocityContext()
        context.put("possession", possession)
        context.put("elements", calculatedElements)
        writer = StringWriter()
        ve.evaluate(context, writer, template.getName(), unicode(template.getSource()))
        evaluatedTemplate = writer.toString()
        return evaluatedTemplate