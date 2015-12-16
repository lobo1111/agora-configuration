import helpers
helpers.init(globals())

from entities.BankCredit import BankCreditManager
bankCreditManager = BankCreditManager()
bankCreditManager.markAsPayed()