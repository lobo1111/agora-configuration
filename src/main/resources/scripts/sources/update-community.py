from entities.Community import CommunityManager

global svars, entityManager, properties
manager = CommunityManager()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.update()