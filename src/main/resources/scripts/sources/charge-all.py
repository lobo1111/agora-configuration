import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from crons.Charger import ChargeManager
chargeManager = ChargeManager()
chargeManager.chargeAll()