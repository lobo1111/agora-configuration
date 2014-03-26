import sys
print sys.path

from crons.AutoPaymentRent import CronAutoPaymentRent

CronAutoPaymentRent().processDocuments()