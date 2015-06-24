import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.BankNote import BankNoteManager
bankNoteManager = BankNoteManager()
bankNoteManager.create()