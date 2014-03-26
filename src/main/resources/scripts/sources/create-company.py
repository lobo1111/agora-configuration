from entities.Company import CompanyManager

global svars, entityManager, properties
companyManager = CompanyManager()
companyManager.setSvars(svars)
companyManager.setEntityManager(entityManager)
companyManager.setProperties(properties)
companyManager.create()