import helpers
helpers.init(globals())

from structures.Account import AccountManager
AccountManager().persist()