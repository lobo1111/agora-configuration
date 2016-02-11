from pl.reaper.container.data import ZakladowyPlanKont
from pl.reaper.container.data import ZpkBalance
from base.Container import Container
from structures.BookingPeriod import BookingPeriodManager
from structures.Dictionary import DictionaryManager

class ZpkManager(Container):
    
    def persist(self):
        zpk = self.findById("ZakladowyPlanKont", self._svars.get('id'))
        self.updateStartCredit(zpk.getCurrentBalance(), self._svars.get('startCredit'))
        self.updateStartDebit(zpk.getCurrentBalance(), self._svars.get('startDebit'))
        self.saveEntity(zpk)
    
    def createZpksForContractor(self, contractor):
        contractor.getZpks().add(self.createZpk(contractor.getCommunity(), "CONTRACTOR"))
        contractor.getZpks().add(self.createZpk(contractor.getCommunity(), "CONTRACTOR_COST"))

    def createDefaultZpkNumbersForCommunity(self, community):
        self.createZpk(community, "CHARGING_RENT")
        self.createZpk(community, "CHARGING_REPAIR_FUND")
        self.createZpk(community, "WAITING_FOR_ACCOUNT")
        self.createZpk(community, "WAITING_FOR_ACCOUNT_RF")
        
    def updateStartCredit(self, balance, startCredit):
        oldStartCredit = balance.getStartCredit()
        balance.setStartCredit(startCredit)
        balance.setCredit(balance.getCredit() - oldStartCredit + startCredit)
        
    def updateStartDebit(self, balance, startDebit):
        oldStartDebit = balance.getStartDebit()
        balance.setStartDebit(startDebit)
        balance.setDebit(balance.getDebit() - oldStartDebit + startDebit)
            
    def createZpk(self, community, type):
        dict = self.findDictionary(str(self.findZpkSettingId(type)))
        type = self.findDictionary(dict.getValue())
        number = self.generateNumber(type, community)
        zpk = ZakladowyPlanKont()
        zpk.setNumber(number)
        zpk.setType(type)
        zpk.setCommunity(community)
        community.getZpks().add(zpk)
        self.setAllBookingPeriods(zpk)
        return zpk
    
    def setAllBookingPeriods(self, zpk):
        bookingPeriodManager = BookingPeriodManager()
        for bookingPeriod in bookingPeriodManager.findAllBookingPeriods():
            balance = ZpkBalance()
            balance.setBookingPeriod(bookingPeriod)
            balance.setZpk(zpk)
            zpk.getZpkBalances().add(balance)

    def generateNumber(self, dict, community):
        zpks = []
        for zpk in community.getZpks():
            if(zpk.getType().getId() == dict.getId()):
                zpks.append(int(zpk.getNumber()))
        for i in range(1, 1000):
            if not i in zpks:
                return self.parseNumber(i)
        return '0'
            
    def parseNumber(self, i):
        if i < 10:
            return '00' + str(i)
        elif i < 100:
            return '0' + str(i)
        return str(i)

    def findZpk(self, zpks, typeKey):
        zpkType = self.findDictionary(str(self.findZpkSettingId(typeKey)))
        return [zpk for zpk in zpks if zpk.getType().getKey() == zpkType.getKey()][0]
            
    def findDictionary(self, id):
        return self.findById('Dictionary', id)
    
    def findZpkSettingId(self, typeKey):
        return DictionaryManager().findDictionaryInstance('ZPKS_SETTINGS', typeKey).getId()