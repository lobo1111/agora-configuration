from pl.reaper.container.data import ZakladowyPlanKont
from pl.reaper.container.data import ZpkBalance
from java.lang import Double

class ZpkManager(Container):
    _logger = Logger([:_scriptId])
    
    def create(self):
        zpk = ZakladowyPlanKont()
        self.setZpkData(zpk)
        self.saveZpk(zpk)
        
    def setZpkData(self, zpk):
        zpk.setNumber(vars.get('number'))
        zpk.setDescription(vars.get('description'))
        zpk.setCommunity(self.getCommunity(zpk))
        zpk.setPossession(self.getPossession(zpk))
        zpk.setPerson(self.getPerson(zpk))
        zpk.setCompany(self.getCompany(zpk))
        self.setAllBookingPeriods(zpk)
        
    def getCommunity(self, zpk):
        if 'communityId' in vars and vars.get('communityId') != '0':
            communityManager = CommunityManager()
            return communityManager.findCommunityById(vars.get('communityId'))
        
    def getPerson(self, zpk):
        if 'personId' in vars and vars.get('personId') != '0':
            personManager = PersonManager()
            return personManager.findPersonById(vars.get('personId'))
        
    def getPossession(self, zpk):
        if 'possessionId'in vars and vars.get('possessionId') != '0':
            possessionManager = PossessionManager()
            return possessionManager.findPossessionById(vars.get('possessionId'))
        
    def getCompany(self, zpk):
        if 'companyId' in vars and vars.get('companyId') != '0':
            companyManager = CompanyManager()
            return companyManager.findCompanyById(vars.get('companyId'))
        
    def setAllBookingPeriods(self, zpk):
        bookingPeriodManager = BookingPeriodManager()
        for bookingPeriod in bookingPeriodManager.findAllBookingPeriods():
            zpkBalance = self.createBalanceForPeriod(bookingPeriod)
            zpk.getZpkBalances().add(zpkBalance)
            
    def createBalanceForPeriod(self, bookingPeriod):
        balance = ZpkBalance()
        balance.setBookingPeriod(bookingPeriod)
        if  bookingPeriod.isDefaultPeriod():
            balance.setCredit(Double.parseDouble(vars.get('credit')))
            balance.setDebit(Double.parseDouble(vars.get('debit')))
            balance.setStartCredit(Double.parseDouble(vars.get('credit')))
            balance.setStartDebit(Double.parseDouble(vars.get('debit')))
        return balance
        
    def saveZpk(self, zpk):
        self._logger.info(zpk.longDescription())
        entityManager.persist(zpk)
        entityManager.flush()
        