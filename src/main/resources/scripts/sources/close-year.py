import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.BookingPeriod import BookingPeriodManager
bookingPeriodManager = BookingPeriodManager()
bookingPeriodManager.closeYear()