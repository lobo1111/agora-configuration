'''
CHANGE TYPE FLOW:
1) 'new type' is UNSET:
    a) In that case current configuration doesn't matter.
        i) Type of edited account is set to UNSET
        *) Community will lose ability to charge !
2) 'new type' is DEFAULT:
    a) There is already an account with DEFAULT type set.
        i) Find existing account with DEFAULT type set and degradate it to
        UNSET type
        ii) Change type of edited account to DEFAULT
    b) There are two functional accounts: RENT and REPAIR_FUND in the collection
        i) Find both functional accounts and degradate then both to UNSET type
        ii) Change type of edited account to DEFAULT
3) 'new type' is RENT:
    a) There is an account with type DEFAULT set.
        i) Find existing account with DEFAULT type set and degradate it to
        UNSET type
        ii) Promote edited account to RENT type
        *) Community will lose ability to charge because there won't be 
        REPAIR_FUND account !
    b) There are two functional accounts: RENT and REPAIR_FUND in the collection
        i) Find current account of type RENT and degradate it to UNSET
        ii) Promote edited account to type RENT
        *) In case that edited account's type is REPAIR_FUND community
        will lose ability to charge !
4) 'new type' is REPAIR_FUND:
    a) There is an account with type DEFAULT set.
        i) Find existing account with DEFAULT type set and degradate it to
        UNSET type
        ii) Promote edited account to RENT type
        *) Community will lose ability to charge because there won't be
        RENT account !
    b) There are two functional accounts: RENT and REPAIR_FUND in the collection
        i) Find current account of type REPAIR_FUND and degradate it to UNSET
        ii) Promote edited account to type REPAIR_FUND
        *) In case that edited account's type is RENT community will lose 
        ability to charge !
        
SIMPLIFIED ALGORITHM:
Above flow can be simplified to just one case:
If new type is UNSET there is really nothing to do except just to set it as
current type which happens for all cases
If new type is different than UNSET then we are always degradating existing
DEFAULT account(if it exists of course) and one or both other functional
accounts(which is RENT and/or REPAIR_FUND). We are degradating both if new
type is DEFAULT or one which is the same type as the new one(RENT for RENT
and REPAIR_FUND for REPAIR_FUND).
To accomplish that we are building a collection of type to degradate in that way:
1) If new type is DEFAULT then collection contains DEFAULT, RENT and REPAIR_FUND
2) If new type is one of the remaining functional accounts then collection
contains: DEFAULT and that new type
Then we are degadating any account from community collection that type is in
that build collection and at the end we are mapping edited account to desired
type.

*** we are searching in whole accounts collection which also contains edited
account, so we have to filter it out. ***

WHY DOES IT WORK:
Case #1 explanation:
If new type is UNSET there is nothing to degradate - except for currently
edited account

Case #2 explanation:
To set new DEFAULT account we have to first find current DEFAULT account
and degradate it. Then we are looking for both functional accounts
and also degradate them. Of course algoritm will find DEFAULT or other two
functional accounts as only one case at the time is possible.

Case #3 explanation:
To set new RENT account we have to degradate existing DEFAULT one(if any)
and existing RENT one(if any) - only one of them can exist so finder will
find only one account to degradate.

Case #4 explanation:
The same as #3 except this time there is REPAIR_FUND instead of RENT
'''
from base.Container import Container

class TypeChangedFlow(Container):
    
    def __init__(self, mapper):
        self._mapper = mapper
        
    def trigger(self):
        if self._mapper.getNewTypeKey() == "DEFAULT":
            toDegradate = ["DEFAULT", "RENT", "REPAIR_FUND"]
        elif self._mapper.getNewTypeKey() == "RENT":
            toDegradate = ["DEFAULT", "RENT"]
        elif self._mapper.getNewTypeKey() == "REPAIR_FUND":
            toDegradate = ["DEFAULT", "REPAIR_FUND"]
        for account in self._mapper.getEntity().getCommunity().getAccounts():
            if not account.equals(self._mapper.getEntity()) and self.toDegradate(account, toDegradate):
                self._logger.info('Degradating account(%d) of type %s' % (account.getId(), account.getType().getKey()))
                self._mapper.unsetType(account)
        self._logger.info('Promoting account(%d)' % (account.getId()))
        self._mapper.mapType()
        
    def toDegradate(self, account, toDegradate):
        return account.getType().getKey() in toDegradate