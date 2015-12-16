import helpers
helpers.init(globals())

from entities.Company import CompanyManager
companyManager = CompanyManager()
companyManager.toggleDefault()