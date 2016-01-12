from base.Container import Container
from entities.Dictionary import DictionaryManager
from entities.BookingPeriod import BookingPeriodManager
from java.io import StringWriter
from org.apache.velocity import VelocityContext
from org.apache.velocity.app import VelocityEngine
from actions.helpers.ChargingRestriction import ChargingRestriction
from actions.helpers.MonthRestriction import MonthRestriction
from actions.helpers.InvoiceRestriction import InvoiceRestriction

class Close(Container):
    
    _restrictions = [ChargingRestriction(), MonthRestriction(), InvoiceRestriction()]
    
    def canCloseMonth(self):
        for restriction in self._restrictions:
            if not restriction.canProceed():
                return False
        return True
    
    def printRestrictionsResult(self):
        template = self.findBy("Template", "name", "'custom-can-close-month'")
        output = self.compileTemplate(template)
        self._svars.put("output", output)
        return output
    
    def compileTemplate(self, template):
        ve = VelocityEngine()
        ve.init()
        context = VelocityContext()
        for restriction in self._restrictions:
            self._logger.info("Checking restriction %s for closing month..." % restriction.getTemplateName())
            restriction.calculate()
            self._logger.info("Restriction result %s" % str(restriction.getResult()))
        context.put("restrictions", self._restrictions)
        context.put("lol", dir(self._restrictions[0]))
        writer = StringWriter()
        ve.evaluate(context, writer, template.getName(), unicode(template.getSource()))
        evaluatedTemplate = writer.toString()
        return evaluatedTemplate
    
    def closeMonth(self):
        if self.canCloseMonth():
            self._logger.info('Closing month...')
            self.bookAll()
            self.setNextMonth()
            self._logger.info('Month closed')
        else:
            self._logger.info("Month can't be closed - at least one of the restrictions failed")
        
    def setNextMonth(self):
        self._nextMonth = int(BookingPeriodManager().getCurrentMonth()) + 1
        dict = DictionaryManager().findDictionaryInstance("PERIODS", "CURRENT")
        dict.setValue(str(self._nextMonth))
        self._saveEntity(dict)
        
    def bookAll(self):
        pass
    