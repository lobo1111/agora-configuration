from entities.ChargingQueue import ChargingQueueManager

global svars, entityManager, properties
chargingQueueManager = ChargingQueueManager()
chargingQueueManager.setSvars(svars)
chargingQueueManager.setEntityManager(entityManager)
chargingQueueManager.setProperties(properties)
chargingQueueManager.addToQueue()