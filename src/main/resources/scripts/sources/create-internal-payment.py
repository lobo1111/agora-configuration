from entities.InternalPayment import InternalPaymentManager

global svars, entityManager, properties
internalPaymentManager = InternalPaymentManager()
internalPaymentManager.setSvars(svars)
internalPaymentManager.setEntityManager(entityManager)
internalPaymentManager.setProperties(properties)
internalPaymentManager.create()