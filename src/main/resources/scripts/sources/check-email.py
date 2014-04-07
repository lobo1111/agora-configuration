import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from loaders.MailProcessor import MailProcessor
mailProcessor = MailProcessor()
mailProcessor.checkMailbox()