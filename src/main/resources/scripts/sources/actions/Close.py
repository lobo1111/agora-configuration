from base.Container import Container
from entities.Dictionary import DictionaryManager
from entities.BookingPeriod import BookingPeriodManager
from java.io import StringWriter
from org.apache.velocity import VelocityContext
from org.apache.velocity.app import VelocityEngine
from actions.helpers.ChargingRestriction import ChargingRestriction
from actions.helpers.MonthRestriction import MonthRestriction
from actions.helpers.YearRestriction import YearRestriction
from actions.helpers.InvoiceRestriction import InvoiceRestriction
from documents.Document import DocumentManager

class Close(Container):
    
    _yearRestrictions = [ChargingRestriction(), YearRestriction(), InvoiceRestriction()]
    _monthRestrictions = [ChargingRestriction(), MonthRestriction(), InvoiceRestriction()]
    _output = dict([])
    
    def canCloseMonth(self):
        return self.canClose(self._monthRestrictions)
    
    def canCloseYear(self):
        return self.canClose(self._yearRestrictions)
    
    def canClose(self, restrictions):
        for restriction in restrictions:
            restriction.calculate()
            if not restriction.getResult():
                return False
        return True
    
    def printMonthRestrictionsResult(self):
        self.printRestrictionsResult(self._monthRestrictions)
        
    def printYearRestrictionsResult(self):
        self.printRestrictionsResult(self._yearRestrictions)
        
    def printRestrictionsResult(self, restrictions):
        template = self.findBy("Template", "name", "'custom-can-close-month'")
        output = self.compileTemplate(template, restrictions)
        self._svars.put("output", output)
        return output
    
    def compileTemplate(self, template, restrictions):
        ve = VelocityEngine()
        ve.init()
        context = VelocityContext()
        context.put("restrictions", self._output)
        for restriction in restrictions:
            restriction.calculate()
            self._output[restriction.getTemplateName()] = [restriction.getTemplateName(), restriction.getResult(), restriction.getMessage()]
        writer = StringWriter()
        ve.evaluate(context, writer, template.getName(), unicode(template.getSource()))
        evaluatedTemplate = writer.toString()
        return evaluatedTemplate
    
    def closeMonth(self):
        if self.canCloseMonth():
            self._logger.info('Closing month...')
            DocumentManager().bookAll()
            self.setNextMonth()
            self._logger.info('Month closed')
        else:
            self._logger.info("Month can't be closed - at least one of the restrictions failed")
        
    def setNextMonth(self):
        self._nextMonth = int(BookingPeriodManager().getCurrentMonth()) + 1
        dict = DictionaryManager().findDictionaryInstance("PERIODS", "CURRENT")
        dict.setValue(str(self._nextMonth))
        self._saveEntity(dict)
    