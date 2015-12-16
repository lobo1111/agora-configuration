import helpers
helpers.init(globals())

from documents.Invoice import InvoiceManager
invoiceManager = InvoiceManager()
invoiceManager.remove()