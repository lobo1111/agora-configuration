import helpers
helpers.init(globals())

from documents.migration.AccountProvision import AccountProvisionMigrator
from documents.migration.BankNote import BankNoteMigrator
from documents.migration.Invoice import InvoiceMigrator
from documents.migration.Charging import ChargingMigrator
invoiceManager = InvoiceMigrator()
#invoiceManager.migrateAll()
noteManager = BankNoteMigrator()
#noteManager.migrateAll()
accountProvision = AccountProvisionMigrator()
#accountProvision.migrateAll()
charging = ChargingMigrator()
charging.migrateAll()