from pl.reaper.container.data import ZakladowyPlanKont
from pl.reaper.container.data import ZpkBalance

class ZpkManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        zpk = ZakladowyPlanKont()
        self.setZpkData(zpk)
        self.saveZpk(zpk)
        
    def setZpkData(self, zpk):
        zpk.setNumber(vars.get('number'))
        zpk.setDescription(vars.get('description'))
        self.setCommunity(self.getCommunity(zpk))
        self.setPossession(self.getPossession(zpk))
        self.setPerson(self.getPerson(zpk))
        self.setCompany(self.getCompany(zpk))
        self.setAllBookingPeriods(zpk)
        
    def getCommunity(self, zpk):
        communityManager = CommunityManager()
        return communityManager.findCommunityById(vars.get('communityId'))
        
    def getPerson(self, zpk):
        if vars.get('personId') != None:
            personManager = PersonManager()
            return personManager.findPersonById(vars.get('personId'))
        
    def getPossession(self, zpk):
        if vars.get('possessionId') != None:
            possessionManager = PossessionManager()
            return possessionManager.findPossessionById(vars.get('possessionId'))
        
    def getCompany(self, zpk):
        if vars.get('companyId') != None:
            companyManager = CompanyManager()
            return companyManager.findCompanyById(vars.get('companyId'))
        
    def setAllBookingPeriods(self, zpk):
        bookingPeriodManager = BookingPeriodManager()
        for bookingPeriod in bookingPeriodManager.findAllBookingPeriods():
            zpkBalance = self.createBalanceForPeriod(bookingPeriod)
            zpk.getZpkBalances.add(zpkBalance)
            
    def createBalanceForPeriod(self, bookingPeriod):
        balance = ZpkBalance()
        if  bookingPeriod.isDefaultPeriod():
            balance.setCredit(vars.get('credit'))
            balance.setDebit(vars.get('debit'))
            balance.setStartCredit(vars.get('credit'))
            balance.setStartDebit(vars.get('debit'))
        self.saveBalance(balance)
        
    def saveZpk(self, zpk):
        self._logger.info(zpk.longDescription())
        entityManager.persist(zpk)
        entityManager.flush()
        
    def saveBalance(self, balance):
        self._logger.info(balance.longDescription())
        entityManager.persist(balance)
        entityManager.flush()
        