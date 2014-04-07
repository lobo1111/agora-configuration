import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.PaymentRent import PaymentRentManager
manager = PaymentRentManager()
manager.removeCharging()