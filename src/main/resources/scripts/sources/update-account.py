import helpers
helpers.init(globals())

from entities.Account import AccountManager
manager = AccountManager()
manager.update()