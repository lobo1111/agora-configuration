import helpers
helpers.init(globals())

from reports.BankAccountsReport import BankAccountsReport
manager = BankAccountsReport()
manager.getReport()