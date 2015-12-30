import helpers
helpers.init(globals())

from documents.migration.AccountProvision import AccountProvisionMigrator
from documents.migration.BankNote import BankNoteMigrator
from documents.migration.Invoice import InvoiceMigrator
invoiceManager = InvoiceMigrator()
#invoiceManager.migrateAll()
noteManager = BankNoteMigrator()
#noteManager.migrateAll()
accountProvision = AccountProvisionMigrator()
accountProvision.migrateAll()