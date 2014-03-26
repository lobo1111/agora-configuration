from entities.ZpksSettings import ZpksSettings

global svars, entityManager, properties
manager = ZpksSettings()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.update()