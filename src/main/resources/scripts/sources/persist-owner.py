import helpers
helpers.init(globals())

from structures.Owner import OwnerManager
OwnerManager().persist()