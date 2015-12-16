import helpers
helpers.init(globals())

from entities.Owner import OwnerManager
ownerManager = OwnerManager()
ownerManager.create()