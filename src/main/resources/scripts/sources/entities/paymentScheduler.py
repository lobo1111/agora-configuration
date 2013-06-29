from pl.reaper.container.data import PaymentScheduler
from pl.reaper.container.data import PaymentSchedulerTemplate

class PaymentSchedulerManager(Container):
    def __init__(self):
        self._dictManager = DictionaryManager()
    
    def create(self):
        paymentScheduler = PaymentScheduler()
        self.setData(paymentScheduler)
        entityManager.persist(paymentScheduler)
        
    def update(self):
        paymentScheduler = self.findPaymentSchedulerById(vars.get('id'))
        self.setData(paymentScheduler)
        entityManager.persist(paymentScheduler)
        
    def setData(self, ps):
        ps.setName(vars.get('paymentSchedulerName'))
        if vars.get('paymentSchedulerActive') == 'true':
            ps.setActive(True)
        else:
            ps.setActive(False)
        ps.setDay(vars.get('paymentSchedulerDay'))
        ps.setCommunity(self.findCommunity(vars.get('communityId')))
        self.setZpks(ps, vars.get('boundedZpksCount'))
        self.setTemplateData(ps)
        
    def setZpks(self, ps, counter):
        ps.getZpks().clear()
        for i in range(int(counter)):
            zpkId = int(vars.get('boundedZpk' + str(i)))
            zpk = self.findZpk(zpkId)
            ps.getZpks().add(zpk)
            
        
    def setTemplateData(self, ps):
        data = self.getOrCreatePaymentSchedulerTemplate(ps)
        data.setPaymentScheduler(ps)
        data.setAlgorithm(self.findAlgorithm())
        data.setAmount(BigDecimal(vars.get('paymentAmount')))
        data.setDescription(vars.get('paymentDescription'))
        data.setType(self.findType(vars.get('paymentType')))
        if vars.get('paymentSchedulerPrefixEnabled') == 'true':
            data.setPrefix(vars.get('paymentSchedulerPrefix'))
        else:
            data.setPrefix(None)
        if vars.get('paymentBook') == 'true':
            data.setAutoBook(True)
        else:
            data.setAutoBook(False)
        ps.getPaymentSchedulerTemplates().clear()
        ps.getPaymentSchedulerTemplates().add(data)
    
    def findCommunity(self, communityId):
        return CommunityManager().findCommunityById(communityId)

    def findAlgorithm(self):
        sql = "Select a From PaymentAlgorithm a Where a.id = %s" % vars.get('algorithmId')
        return entityManager.createQuery(sql).getSingleResult() 
    
    def findType(self, typeId):
        return self._dictManager.getDictionaryInstance(typeId)
    
    def findZpk(self, zpkId):
        return ZpkManager().findZpkById(zpkId)
    
    def findPaymentSchedulerById(self, psId):
        sql = "Select ps From PaymentScheduler ps Where ps.id = '%s'" % psId
        return entityManager.createQuery(sql).getSingleResult()
    
    def getOrCreatePaymentSchedulerTemplate(self, entity):
        if entity.getPaymentSchedulerTemplates().size() == 1:
            return entity.getPaymentSchedulerTemplates().get(0)
        else:
            return PaymentSchedulerTemplate()
    