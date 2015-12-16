import helpers
helpers.init(globals())

from entities.AccountProvision import AccountProvisionManager
manager = AccountProvisionManager()
manager.create()