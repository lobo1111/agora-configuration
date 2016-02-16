'''
ACTIONS SUPPORTED BY ACCOUNT MANAGER:
    - persist
    - close[TODO]
    
USAGE OF OTHER STRUCTURES:
    - CompanyManager: for handling Bank data
    - ZpkManager: for managing account's ZPKs
    
PERSIST PROCESS:

Account data always comes with bank data. Bank data is represented by company standard,
so it's collected by CompanyManager structure. Account holds bank data in two ways:
1) as a reference to Bank entity; 2) as a reference to Contractor entity(which is connected
to company represented by this Bank).
Details of handling changes on company data is covered in CompanyManager structure.
This structure just benefits of that process and uses it to create Bank and Contractor
references.

ON ADD:
Core data is set: Bank and Contractor reference; account number; community reference;
type of the account; zpks for selected type.

ON EDIT:
Most of the core data can't be changed. Bank and Contractor entities are static(
except for company details). Account number is also static. Only property that
can be changed is account type and triggers a complicated process. 

*** In case of 'new type' == 'old type' change is ignored. ***

*** In case of a promotion to a function account - ZPKs are automatically
generated by ZPK Manager, unless account already has them. That can occur if
edited account already was bound to that type in the past(ZPKs are never removed)
or new type is a subset of old one(e.g. DEFAULT -> RENT or REPAIR_FUND). ***

CHANGE TYPE FLOW:
Full flow of changed type process is explained in 
structures.helpers.account.TypeChangedFlow
'''
from base.Container import Container
from structures.helpers.account.Mapper import AccountMapper
from structures.helpers.account.TypeChangedFlow import TypeChangedFlow
from structures.helpers.account.BankDataHelper import BankDataHelper

class AccountManager(Container):

    def persist(self):
        '''
        Mapper initializes account entity - creates new one in case of 'add' 
        action or loads existing one in case if 'edit' action
        '''
        mapper = AccountMapper()
        mapper.initStructure()
        if mapper.isNew():
            '''
            New structure is created, account data is set by mapper,
            ZpkManager generates new ZPK accounts.
            '''
            mapper.setData()
            ZpkManager().createZpksForAccount(account)
        elif mapper.typeChanged():
            '''
            Structure is changed and there is new type - workflow gets triggered.
            Afterwards ZpkManager creates appropriate ZPKs if any is missing.
            '''
            TypeChangedFlow(mapper).trigger()
            ZpkManager().createZpksForAccount(account)
        else:
            '''
            Structure already exists but account type remains, so likely
            it was 'false' save or just Bank data was changed(which was
            already applied above).
            '''
            pass
        '''
        BankDataHelper handles bank data based on bank code found in account
        number. If bank with that code already exists it just update it's
        company record(both CompanyManager and ContractorManager supports
        getOrCreate method) otherwise it creates a new Bank with provided data.
        '''
        BankDataHelper().handleData(self._entity)
