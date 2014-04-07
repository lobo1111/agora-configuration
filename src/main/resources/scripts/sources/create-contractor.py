import helpers
helpers.entityManager = globals()['entityManager']
helpers.svars = globals()['svars']
helpers.properties = globals()['properties']

from entities.Contractor import ContractorManager
contractorManager = ContractorManager()
contractorManager.create()