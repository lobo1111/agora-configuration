import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.Invoice import InvoiceManager
invoiceManager = InvoiceManager()
invoiceManager.update()