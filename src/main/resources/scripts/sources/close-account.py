import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.Account import AccountManager
accountManager = AccountManager()
accountManager.close()