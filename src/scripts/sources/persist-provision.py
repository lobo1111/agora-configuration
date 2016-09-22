import helpers
helpers.init(globals())

from documents.AccountProvision import AccountProvisionManager
AccountProvisionManager().persist()