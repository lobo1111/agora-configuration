import helpers
helpers.init(globals())

from documents.BankNote import BankNoteManager
bankNoteManager = BankNoteManager()
bankNoteManager.cancel()