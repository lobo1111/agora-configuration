import helpers
helpers.init(globals())

from actions.ClosePeriod import ClosePeriodManager
ClosePeriodManager().close()