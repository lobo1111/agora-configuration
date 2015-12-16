import helpers
helpers.init(globals())

from entities.Invoice import InvoiceManager
invoiceManager = InvoiceManager()
invoiceManager.cancel()