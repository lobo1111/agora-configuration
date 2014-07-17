import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.BankStatement import BankStatementManager
bankStatementManager = BankStatementManager()
bankStatementManager.create()