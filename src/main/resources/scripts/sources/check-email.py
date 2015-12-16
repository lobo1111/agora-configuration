import helpers
helpers.init(globals())

from loaders.MailProcessor import MailProcessor
mailProcessor = MailProcessor()
mailProcessor.checkMailbox()