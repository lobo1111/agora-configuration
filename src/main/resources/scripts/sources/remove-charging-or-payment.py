import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

print globals()['svars'].get('id')
if int(globals()['svars'].get('id')) < 0:
    id = int(globals()['svars'].get('id') * -1)
    print '-' + id + '-'
    globals()['svars'].put('id', str(id))
    from entities.PaymentRent import PaymentRentManager
    manager = PaymentRentManager()
    manager.removeCharging()
elif globals()['svars'].get('id').startswith('PAYMENT_RENT'):
    from entities.PaymentRent import PaymentRentManager
    manager = PaymentRentManager()
    manager.remove()