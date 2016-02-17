from base.Container import Container
from pl.reaper.container.data import Bank
from structures.Company import CompanyManager

class BankManager(Container):

    '''
    Extracts Bank entity based on provided account number. If such bank doesn't
    exists it's created.
    '''
    def getBankFromAccountNumber(self, number):
        bankCode = number[2:6]
        bank = self.findBy('Bank', 'key', '"' + bankCode + '"')
        if bank == None:
            bank = Bank()
            bank.setKey(bankCode)
            bank.setName(company.getName())
        CompanyManager().set(bank)
        return bank