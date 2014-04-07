import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.Possession import PossessionManager
manager = PossessionManager()
manager.create()