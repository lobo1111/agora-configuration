from entities.Contractor import ContractorManager

global svars, entityManager, properties
contractorManager = ContractorManager()
contractorManager.setSvars(svars)
contractorManager.setEntityManager(entityManager)
contractorManager.setProperties(properties)
contractorManager.create()