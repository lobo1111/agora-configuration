import helpers
helpers.init(globals())

from actions.ChargingReport import ChargingReport
manager = ChargingReport()
manager.create()