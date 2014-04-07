import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.Bank import BankManager
bankManager = BankManager()
bankManager.create()