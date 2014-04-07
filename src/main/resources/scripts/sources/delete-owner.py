import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.Owner import OwnerManager
manager = OwnerManager()
manager.delete()