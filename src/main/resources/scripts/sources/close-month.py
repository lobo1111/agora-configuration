from actions.Close import Close

global svars, entityManager, properties
close = Close()
close.setSvars(svars)
close.setEntityManager(entityManager)
close.setProperties(properties)
close.closeMonth()