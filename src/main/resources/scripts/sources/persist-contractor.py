import helpers
helpers.init(globals())

from structures.Contractor import ContractorManager
ContractorManager().persist()