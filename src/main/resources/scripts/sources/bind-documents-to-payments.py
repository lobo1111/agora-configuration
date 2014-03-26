from crons.AutoPaymentRent import CronAutoPaymentRent

global svars 
cronAutoPaymentRent = CronAutoPaymentRent()
CronAutoPaymentRent.setSvars(svars)
CronAutoPaymentRent.processDocuments()