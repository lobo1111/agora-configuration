import helpers
helpers.init(globals())

from actions.User import User
manager = User()
manager.getUserInformation()