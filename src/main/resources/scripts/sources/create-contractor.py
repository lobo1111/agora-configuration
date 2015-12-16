import helpers
helpers.init(globals())

from entities.Contractor import ContractorManager
contractorManager = ContractorManager()
contractorManager.create()