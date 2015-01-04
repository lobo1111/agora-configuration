import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.Zpk import ZpkManager
manager = ZpkManager()
manager.setStartBalance()