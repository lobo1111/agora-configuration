import helpers
helpers.init(globals())

from entities.Community import CommunityManager
communityManager = CommunityManager()
communityManager.decomission()