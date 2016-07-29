import helpers
helpers.init(globals())

from reports.ZpksStatusReport import ZpksStatusReport
manager = ZpksStatusReport()
manager.getReport()