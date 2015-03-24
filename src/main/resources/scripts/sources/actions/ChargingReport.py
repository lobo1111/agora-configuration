from base.Container import Container
from crons.Charger import Calculator
from entities.BookingPeriod import BookingPeriodManager
from pl.reaper.container.data import ChargingElement
from java.io import StringWriter
from org.apache.velocity import VelocityContext
from org.apache.velocity.app import VelocityEngine

class ChargingReport(Container):

    def create(self):
        possession = self.findById("Possession", self._svars.get("id"))
        template = self.findBy("Template", "name", "'charging-report'")
        calculatedElements = self.calculateElements(possession)
        output = self.compileTemplate(template, possession, calculatedElements)
        self._svars.put("output", output)
        return output

    def calculateElements(self, possession):
        calculatedElements = []
        for element in possession.getElements():
            element.getElement().setGlobalValue(self.discoverValue(element))
            calculator = Calculator()
            cElement = ChargingElement()
            cElement.setName(element.getElement().getName())
            cElement.setGroup(element.getElement().getGroup())
            cElement.setValue(calculator.calculate(element.getElement(), possession))
            calculatedElements.append(cElement)
        return calculatedElements

    def compileTemplate(self, template, possession, calculatedElements):
        ve = VelocityEngine()
        ve.init()
        context = VelocityContext()
        context.put("possession", possession)
        context.put("elements", calculatedElements)
        context.put("bookingPeriod", BookingPeriodManager().findDefaultBookingPeriod())
        writer = StringWriter()
        ve.evaluate(context, writer, template.getName(), unicode(template.getSource()))
        evaluatedTemplate = writer.toString()
        return evaluatedTemplate

    def discoverValue(self, possessionElement):
        if possessionElement.isOverrideParentValue():
            return possessionElement.getGlobalValue()
        elif possessionElement.getElementCommunity() != None and possessionElement.getElementCommunity().isOverrideParentValue():
            return possessionElement.getElementCommunity().getGlobalValue()
        else:
            return possessionElement.getElement().getGlobalValue()