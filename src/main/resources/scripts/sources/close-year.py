import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from actions.BookingPeriod import BookingPeriodManager
bookingPeriodManager = BookingPeriodManager()
bookingPeriodManager.closeYear()