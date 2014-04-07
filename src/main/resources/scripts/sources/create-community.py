import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.Community import CommunityManager
communityManager = CommunityManager()
communityManager.create()