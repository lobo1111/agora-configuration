import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.ChargingQueue import ChargingQueueManager
chargingQueueManager = ChargingQueueManager()
chargingQueueManager.addToQueue()