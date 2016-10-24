import helpers
helpers.init(globals())

from documents.Invoice import InvoiceManager
InvoiceManager().persistPayment()