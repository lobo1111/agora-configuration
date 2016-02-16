from base.Container import Container
from structures.Bank import BankManager
from structures.Contractor import ContractorManager

'''
Help to handle Bank data on account persist. Helper doesn't know which action
was trigger 'add' or 'edit'. There is no need for that. Both BankManager
and ContractorManager supports getOrCreate methods. No duplicates are
created.
'''
class BankDataHelper(Container):
    
    def handleData(self, account):
        bank = BankManager().getBankFromAccountNumber(account.getNumber())
        self._logger.info("Assigned Bank - %s, for acount: %s" % (bank.getName(), account.getNumber()))
        contractor = ContractorManager().getOrCreateContractor(bank.getCompany())
        account.setBank(bank)
        account.setBankContractor(contractor)
        