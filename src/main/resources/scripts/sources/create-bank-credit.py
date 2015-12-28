import helpers
helpers.init(globals())

from documents.BankCredit import BankCreditManager
bankCreditManager = BankCreditManager()
bankCreditManager.create()