import helpers
helpers.init(globals())

from crons.Charger import ChargeManager
chargeManager = ChargeManager()
chargeManager.chargeAll()