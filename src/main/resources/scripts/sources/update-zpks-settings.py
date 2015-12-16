import helpers
helpers.init(globals())

from entities.ZpksSettings import ZpksSettings
manager = ZpksSettings()
manager.update()