from entities.Zpk import ZpkManager

global svars, entityManager, properties
manager = ZpkManager()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.create()