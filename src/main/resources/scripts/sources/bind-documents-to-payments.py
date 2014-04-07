import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from crons.AutoPaymentRent import CronAutoPaymentRent
cronAutoPaymentRent = CronAutoPaymentRent()
cronAutoPaymentRent.processDocuments()