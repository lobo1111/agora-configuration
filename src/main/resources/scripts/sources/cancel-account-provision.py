import helpers
helpers.init(globals())

from documents.AccountProvision import AccountProvisionManager
manager = AccountProvisionManager()
manager.cancel()