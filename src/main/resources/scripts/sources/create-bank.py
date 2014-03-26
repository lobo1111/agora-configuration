from entities.Bank import BankManager

global svars, entityManager, properties
bankManager = BankManager()
bankManager.setSvars(svars)
bankManager.setEntityManager(entityManager)
bankManager.setProperties(properties)
bankManager.create()