import helpers
helpers.init(globals())

from crons.AutoPaymentRent import CronAutoPaymentRent
cronAutoPaymentRent = CronAutoPaymentRent()
cronAutoPaymentRent.processDocuments()