import helpers
helpers.init(globals())

from entities.ZpkDictionary import ZpkDictionaryManager
manager = ZpkDictionaryManager()
manager.create()