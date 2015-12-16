import helpers
helpers.init(globals())

from entities.BankStatement import BankStatementManager
bankStatementManager = BankStatementManager()
bankStatementManager.create()