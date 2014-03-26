from entities.Account import AccountManager

global svars, entityManager, properties
manager = AccountManager()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.update()