import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.InternalPayment import InternalPaymentManager
internalPaymentManager = InternalPaymentManager()
internalPaymentManager.cancel()