import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.BankCredit import BankCreditManager
bankCreditManager = BankCreditManager()
bankCreditManager.markAsPayed()