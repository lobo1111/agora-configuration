import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.Element import ElementManager
elementManager = ElementManager()
elementManager.multiUpdate()