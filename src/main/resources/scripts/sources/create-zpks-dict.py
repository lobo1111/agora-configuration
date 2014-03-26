from entities.ZpkDitctionary import ZpkDictionaryManager

global svars, entityManager, properties
manager = ZpkDictionaryManager()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.create()