import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.Company import CompanyManager
companyManager = CompanyManager()
companyManager.toggleDefault()