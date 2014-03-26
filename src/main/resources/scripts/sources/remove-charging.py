from entities.PaymentRent import PaymentRentManager

global svars, entityManager, properties
manager = PaymentRentManager()
manager.setSvars(svars)
manager.setEntityManager(entityManager)
manager.setProperties(properties)
manager.removeCharging()