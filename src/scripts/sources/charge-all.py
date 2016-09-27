import helpers
helpers.init(globals())

from documents.Charger import ChargerManager
ChargerManager().chargeAll()