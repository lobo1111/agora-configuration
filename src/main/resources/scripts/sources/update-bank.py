from entities.Bank import BankManager

global svars, entityManager, properties
manager = BankManager()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.update()