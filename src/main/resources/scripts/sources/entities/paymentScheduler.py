from pl.reaper.container.data import PaymentScheduler
from pl.reaper.container.data import PaymentSchedulerTemplate

class PaymentSchedulerManager(Container):
    def __init__(self):
        self._dictManager = DictionaryManager()
    
    def create(self):
        paymentScheduler = PaymentScheduler()
        self.setData(paymentScheduler)
        entityManager.persist(paymentScheduler)
        
    def setData(self, ps):
        ps.setName(vars.get('paymentSchedulerName'))
        if vars.get('paymentSchedulerActive') == 'true':
            ps.setActive(True)
        ps.setDay(vars.get('paymentSchedulerDay'))
        ps.setCommunity(self.findCommunity(vars.get('communityId')))
        self.setTemplateData(ps)
        
    def setTemplateData(self, ps):
        data = PaymentSchedulerTemplate()
        data.setAmount(BigDecimal(vars.get('paymentAmount')))
        data.setAccount(self.findAccount(vars.get('accountId')))
        data.setDescription(vars.get('paymentDescription'))
        data.setType(self.findType(vars.get('paymentType')))
        if vars.get('paymentBook') == 'true':
            data.setAutoBook(True)
        data.setZpk(self.findZpk(vars.get('zpkId')))
        data.setBookingPeriod(self.findBookingPeriod(vars.get('paymentBookingPeriod')))
        ps.getPaymentSchedulerTemplates().clear()
        ps.getPaymentSchedulerTemplates().add(data)
    
    def findCommunity(self, communityId):
        return CommunityManager().findCommunityById(communityId)
    
    def findAccount(self, accountId):
        return AccountManager().findAccountById(accountId)
    
    def findType(self, typeId):
        self._dictManager.getDictionaryInstance(typeId)
    
    def findZpk(self, zpkId):
        return ZpkManager().findZpkById(zpkId)
    
    def findBookingPeriod(self, periodId):
        return BookingPeriodManager().findBookingPeriodById(periodId)
    