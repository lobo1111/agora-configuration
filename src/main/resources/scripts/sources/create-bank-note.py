import helpers
helpers.init(globals())

from entities.BankNote import BankNoteManager
bankNoteManager = BankNoteManager()
bankNoteManager.create()