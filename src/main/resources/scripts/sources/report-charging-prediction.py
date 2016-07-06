import helpers
helpers.init(globals())

from reports.ChargingPredictionReport import ChargingPredictionReport
manager = ChargingPredictionReport()
manager.getReport()