from structures.Company import CompanyManager
from structures.Contractor import ContractorManager

class BankDataHelper(Container):
    
    def handleData(self, account):
        company = CompanyManager().findOrCreate()
        CompanyManager().setData(company)
        contractor = ContractorManager().getOrCreateContractor(company)
        account.setBank(company)
        account.setBankContractor(contractor)
        