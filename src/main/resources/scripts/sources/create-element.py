from entities.Element import ElementManager

global svars, entityManager, properties
elementManager = ElementManager()
elementManager.setSvars(svars)
elementManager.setEntityManager(entityManager)
elementManager.setProperties(properties)
elementManager.create()