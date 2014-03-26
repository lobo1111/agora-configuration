from entities.Person import PersonManager

global svars, entityManager, properties
manager = PersonManager()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.update()