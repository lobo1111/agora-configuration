import helpers
helpers.init(globals())

from entities.Community import CommunityManager
manager = CommunityManager()
manager.update()