import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.AccountProvision import AccountProvisionManager
manager = AccountProvisionManager()
manager.remove()