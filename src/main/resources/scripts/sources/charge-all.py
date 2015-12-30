import helpers
helpers.init(globals())

from documents.Charger import ChargeManager
chargeManager = ChargeManager()
chargeManager.chargeAll()