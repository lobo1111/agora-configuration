import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

if globals()['svars'].get('id').startswith('CHARGE'):
    id = globals()['svars'].get('id')[7:]
    globals()['svars'].put('id', id)
    from entities.PaymentRent import PaymentRentManager
    manager = PaymentRentManager()
    manager.removeCharging()
elif globals()['svars'].get('id').startswith('PAYMENT_RENT'):
    id = globals()['svars'].get('id')[13:]
    globals()['svars'].put('id', id)
    from entities.PaymentRent import PaymentRentManager
    manager = PaymentRentManager()
    manager.remove()