import helpers
helpers.init(globals())

from documents.PaymentRent import PaymentRentManager
PaymentRentManager().create()