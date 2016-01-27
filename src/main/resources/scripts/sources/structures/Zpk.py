from pl.reaper.container.data import ZakladowyPlanKont
from pl.reaper.container.data import ZpkBalance
from base.Container import Container
from structures.BookingPeriod import BookingPeriodManager

class ZpkManager(Container):
    
    def createZpksForContractor(self, contractor):
        contractor.getZpks().add(self.createZpk(contractor.getCommunity(), "CONTRACTOR"))
        contractor.getZpks().add(self.createZpk(contractor.getCommunity(), "CONTRACTOR_COST"))

    def createDefaultZpkNumbersForCommunity(self, community):
        self.createZpk(community, "CHARGING_RENT")
        self.createZpk(community, "CHARGING_REPAIR_FUND")
        self.createZpk(community, "WAITING_FOR_ACCOUNT")
        self.createZpk(community, "WAITING_FOR_ACCOUNT_RF")
            
    def createZpk(self, community, type):
        dict = self.findDictionary(str(self.findZpkSettingId(type)))
        number = self.generateNumber(dict, community)
        zpk = ZakladowyPlanKont()
        zpk.setNumber(number)
        zpk.setType(dict)
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
            zpk.getZpkBalances().add(zpkBalance)

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
        return DictionaryManager().findDictionaryInstance('ZPKS_SETTINGS', typeKey)