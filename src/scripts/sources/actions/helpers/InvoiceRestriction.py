from actions.helpers.Restriction import Restriction

class InvoiceRestriction(Restriction):
    
    def calculate(self):
        notAcceptedInvoices = self.countNotAcceptedInvoices()
        return (notAcceptedInvoices == 0)
        
    def countNotAcceptedInvoices(self):
        sql = "Select count(invoice) From Document invoice Join invoice.attributes attr Where invoice.type = 'INVOICE' And attr.name = 'ACCEPTED' And attr.value = 'false' and invoice.community.inDate != null and invoice.community.outDate = null"
        return self._entityManager.createQuery(sql).getSingleResult()