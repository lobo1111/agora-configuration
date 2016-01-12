import helpers
helpers.init(globals())

from actions.Close import Close
manager = Close()
manager.printRestrictionsResult()