from loaders.FileWatchdog import FileWatchdog

global svars, entityManager, properties
manager = FileWatchdog()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.processFiles()