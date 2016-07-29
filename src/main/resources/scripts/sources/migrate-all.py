import helpers
helpers.init(globals())

from documents.migration.AccountProvision import AccountProvisionMigrator
from documents.migration.BankNote import BankNoteMigrator
from documents.migration.Invoice import InvoiceMigrator
from documents.migration.Charger import ChargerMigrator
from documents.migration.PaymentRent import PaymentRentMigrator
invoiceManager = InvoiceMigrator()
invoiceManager.migrateAll()
noteManager = BankNoteMigrator()
noteManager.migrateAll()
accountProvision = AccountProvisionMigrator()
accountProvision.migrateAll()
charging = ChargerMigrator()
charging.migrateAll()
pr = PaymentRentMigrator()
pr.migrateAll()