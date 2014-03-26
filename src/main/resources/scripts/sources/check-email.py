from loaders.MailProcessor import MailProcessor

global svars, entityManager, properties
mailProcessor = MailProcessor()
mailProcessor.setSvars(svars)
mailProcessor.setEntityManager(entityManager)
mailProcessor.setProperties(properties)
mailProcessor.checkMailbox()