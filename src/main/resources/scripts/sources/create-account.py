from entities.Account import AccountManager

global svars, entityManager, properties
accountManager = AccountManager()
accountManager.setSvars(svars)
accountManager.setEntityManager(entityManager)
accountManager.setProperties(properties)
accountManager.create()