from actions.helpers.Restriction import Restriction

class InvoiceRestriction(Restriction):
    
    def calculate(self):
        notAcceptedInvoices = self.countNotAcceptedInvoices()
        if notAcceptedInvoices == 0:
           self._result = True
        else:
            self._message = "Należy zatwierdzić wszystkie faktury - brakuje %d akceptacji" % (notAcceptedInvoices)
            self._result = False
        
    def countNotAcceptedInvoices(self):
        sql = "Select count(invoice) From Invoice invoice Join invoice.attributes attr Where attr.name = 'ACCEPTED', And attr.value = 'false'"
        return self._entityManager.createQuery(sql).getSingleResult()
    
    def getTemplateName(self):
        return "invoice"
    