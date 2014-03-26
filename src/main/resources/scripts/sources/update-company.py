from entities.Company import CompanyManager

global svars, entityManager, properties
manager = CompanyManager()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.update()