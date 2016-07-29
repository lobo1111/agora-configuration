import helpers
helpers.init(globals())

from reports.ZpkTransactionsReport import ZpkTransactionsReport
manager = ZpkTransactionsReport()
manager.getReport()