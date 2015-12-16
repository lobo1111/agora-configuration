import helpers
helpers.init(globals())

from entities.BookingPeriod import BookingPeriodManager
bookingPeriodManager = BookingPeriodManager()
bookingPeriodManager.closeYear()