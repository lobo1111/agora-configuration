import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from actions.ChargingReport import ChargingReport
manager = ChargingReport()
manager.create()