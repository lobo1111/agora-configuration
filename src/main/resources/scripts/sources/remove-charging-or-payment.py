import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

if int(globals()['svars'].get('id')) < 0:
    id = int(globals()['svars'].get('id') * -1)
    globals()['svars'].put('id', str(id))
    from entities.PaymentRent import PaymentRentManager
    manager = PaymentRentManager()
    manager.removeCharging()
else:
    from entities.PaymentRent import PaymentRentManager
    manager = PaymentRentManager()
    manager.remove()