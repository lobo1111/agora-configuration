import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.ZpkDictionary import ZpkDictionaryManager
manager = ZpkDictionaryManager()
manager.create()