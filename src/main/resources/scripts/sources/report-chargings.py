import helpers
helpers.init(globals())

from reports.ChargingsReport import ChargingsReport
manager = ChargingsReport()
manager.getReport()