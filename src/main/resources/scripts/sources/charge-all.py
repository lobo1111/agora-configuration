import helpers
helpers.init(globals())

from documents.Charger import ChargerManager
chargeManager = ChargerManager()
chargeManager.chargeAll()