import helpers
helpers.init(globals())

from loaders.FileWatchdog import FileWatchdog
manager = FileWatchdog()
manager.processFiles()