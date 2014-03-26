from entities.Element import ElementManager

global svars, entityManager, properties
manager = ElementManager()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.removeSubElement()