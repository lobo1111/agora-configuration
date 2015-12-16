import helpers
helpers.init(globals())

from entities.Account import AccountManager
accountManager = AccountManager()
accountManager.close()