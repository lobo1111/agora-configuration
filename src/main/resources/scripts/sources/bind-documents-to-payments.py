from crons.AutoPaymentRent import CronAutoPaymentRent

global svars 
cronAutoPaymentRent = CronAutoPaymentRent()
cronAutoPaymentRent.setSvars(svars)
cronAutoPaymentRent.processDocuments()