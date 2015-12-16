import helpers
helpers.init(globals())

from entities.Owner import OwnerManager
manager = OwnerManager()
manager.delete()