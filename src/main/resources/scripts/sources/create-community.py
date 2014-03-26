from entities.Community import CommunityManager

global svars, entityManager, properties
communityManager = CommunityManager()
communityManager.setSvars(svars)
communityManager.setEntityManager(entityManager)
communityManager.setProperties(properties)
communityManager.create()