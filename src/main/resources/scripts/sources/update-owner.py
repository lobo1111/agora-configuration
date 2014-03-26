from entities.Owner import OwnerManager

global svars, entityManager, properties
manager = OwnerManager()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.update()