import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from loaders.FileWatchdog import FileWatchdog
manager = FileWatchdog()
manager.processFiles()