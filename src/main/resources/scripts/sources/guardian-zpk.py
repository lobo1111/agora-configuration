import helpers
helpers.init(globals())

from crons.GuardianZpks import GuardianZpk
GuardianZpk().checkAll()