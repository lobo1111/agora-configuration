import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.ZpksSettings import ZpksSettings
manager = ZpksSettings()
manager.update()