from entities.Possession import PossessionManager

global svars, entityManager, properties
manager = PossessionManager()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.create()