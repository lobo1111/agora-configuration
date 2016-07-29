import helpers
helpers.init(globals())

from structures.CommunityDetails import CommunityDetailsManager
CommunityDetailsManager().persist()