from crons.AutoPaymentRent import CronAutoPaymentRent

global svars, entityManager, properties
cronAutoPaymentRent = CronAutoPaymentRent()
cronAutoPaymentRent.setSvars(svars)
cronAutoPaymentRent.setEntityManager(entityManager)
cronAutoPaymentRent.setProperties(properties)
cronAutoPaymentRent.processDocuments()