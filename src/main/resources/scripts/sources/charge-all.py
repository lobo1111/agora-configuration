from crons.Charger import ChargeManager

global svars, entityManager, properties
chargeManager = ChargeManager()
chargeManager.setSvars(svars)
chargeManager.setEntityManager(entityManager)
chargeManager.setProperties(properties)
chargeManager.chargeAll()