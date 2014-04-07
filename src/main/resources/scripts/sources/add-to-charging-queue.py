import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.ChargingQueue import ChargingQueueManager

global svars, entityManager, properties
chargingQueueManager = ChargingQueueManager()
#chargingQueueManager.setSvars(svars)
#chargingQueueManager.setEntityManager(entityManager)
#chargingQueueManager.setProperties(properties)
chargingQueueManager.addToQueue()