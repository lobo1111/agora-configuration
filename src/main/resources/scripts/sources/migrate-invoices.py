import helpers
helpers.init(globals())

from documents.migration.Invoice import InvoiceMigrator
invoiceManager = InvoiceMigrator()
invoiceManager.migrateAll()