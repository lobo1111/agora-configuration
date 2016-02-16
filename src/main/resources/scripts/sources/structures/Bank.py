from base.Container import Container
from pl.reaper.container.data import Bank

class BankManager(Container):

    '''
    Extracts Bank entity based on provided account number. If such bank doesn't
    exists it's created.
    '''
    def getBankFromAccountNumber(self, number):
        bankCode = number[2:6]
        company = CompanyManager().findOrCreate()
        CompanyManager().setData(company)
        bank = self.findBy('Bank', 'key', '"' + bankCode + '"')
        if bank == None:
            bank = Bank()
            bank.setKey(bankCode)
            bank.setCompany(company)
            bank.setName(company.getName())
        return bank