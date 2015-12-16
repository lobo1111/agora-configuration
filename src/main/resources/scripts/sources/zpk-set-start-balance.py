import helpers
helpers.init(globals())

from entities.Zpk import ZpkManager
manager = ZpkManager()
manager.setStartBalance()