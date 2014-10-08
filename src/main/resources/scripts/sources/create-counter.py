import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.Counter import CounterManager
counterManager = CounterManager()
counterManager.create()